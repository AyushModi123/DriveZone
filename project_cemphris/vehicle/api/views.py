from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from base.permissions import IsInstructorPermission, IsLearnerPermission, RequiredProfileCompletionPermission
from base.models import User, ProfileCompletionLevelChoices
from vehicle.models import Vehicle
from .serializers import InstructorVehicleSerializer, LearnerVehicleSerializer
from firebase_utils import FirebaseUploadImage


@swagger_auto_schema(
    method='post',
    request_body=InstructorVehicleSerializer,    
)
@api_view(['POST'])
@permission_classes([IsInstructorPermission, RequiredProfileCompletionPermission(required_level=ProfileCompletionLevelChoices.BASIC)])
def create_vehicle(request):
    serializer = InstructorVehicleSerializer(data=request.data)
    if serializer.is_valid():
        image_file = request.FILES.get('image', None)
        if image_file:
            img_url = FirebaseUploadImage.upload_image(image_file, 'vehicles')
            vehicle = serializer.save(
                image_url=img_url, 
                instructor=request.user.instructor
            )
        else:
            vehicle = serializer.save(
                instructor=request.user.instructor
            )
        return Response({'message': 'Vehicle Saved', 'vehicle_id': vehicle.id}, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
def get_vehicle(request):
    current_user = request.user
    vehicle_id = request.GET.get('id', None)
    try:
        vehicle = Vehicle.objects.get(id=vehicle_id)
    except Vehicle.DoesNotExist:
        return Response({
            'error': 'Vehicle Not Found'
        }, status=404
    )
    if current_user.is_learner:                    
            return Response({
                'vehicle': LearnerVehicleSerializer(vehicle).data
                }, status=200
            )
    elif current_user.is_instructor:        
        return Response({
            'slots': InstructorVehicleSerializer(vehicle).data
            },
            status=200
        )
    else:
        pass


@api_view(['POST'])
@permission_classes([IsInstructorPermission, RequiredProfileCompletionPermission(required_level=ProfileCompletionLevelChoices.BASIC)])
def upload_image(request):
    image_file = request.FILES.get('image', None)
    vehicle_id = request.GET.get('vehicle_id', None) #Query Params
    if image_file:
        try:            
            vehicle = Vehicle.objects.get(id=vehicle_id)
        except Vehicle.DoesNotExist:
            return Response({'error': 'Invalid Vehicle Id'}, status=400)
        img_url = FirebaseUploadImage.upload_image(image_file, 'vehicles')
        vehicle.image_url = img_url
        vehicle.save()
        return Response({'message': 'Image Uploaded', 'vehicle_id': vehicle.id}, status=200)
    else:
        return Response({'error': 'Invalid Image File'}, status=400)