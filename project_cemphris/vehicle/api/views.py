from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from base.permissions import IsSchoolPermission, IsLearnerPermission, RequiredProfileCompletionPermission
from base.models import User, ProfileCompletionLevelChoices
from vehicle.models import Vehicle
from .serializers import VehicleSerializer, OutShortVehicleSerializer
from firebase_utils import FirebaseUploadImage



class VehicleView(APIView):
    def get_permissions(self):
        if self.request.method in ('POST', 'PUT'):
            return [IsSchoolPermission, RequiredProfileCompletionPermission(required_level=50)]
        return [IsSchoolPermission]

    def get(self, request):
        q = request.GET.get("q", "")
        vehicles = Vehicle.objects.filter(
            Q(model__icontains=q) | 
            Q(license_no__icontains=q) |
            Q(make__icontains=q) |
            Q(type__icontains=q)
        )
        return Response({'vehicles': OutShortVehicleSerializer(vehicles, many=True).data}, status=200)

    def post(self, request):
        serializer = VehicleSerializer(data=request.data)
        image_file = request.FILES.get('image', None)
        if image_file:
            if serializer.is_valid():            
                img_url = FirebaseUploadImage.upload_image(image_file, 'vehicles')
                vehicle = serializer.save(
                    image_url=img_url, 
                    school=request.user.school
                )
                return Response({'message': 'Vehicle Saved', 'vehicle_id': vehicle.id}, status=201)
            else:
                return Response(serializer.errors, status=400)
        else:
            return Response({'error': 'Invalid Image File'}, status=400)

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
                'vehicle': VehicleSerializer(vehicle).data
                }, status=200
            )
    elif current_user.is_school:        
        return Response({
            'vehicle': VehicleSerializer(vehicle).data
            },
            status=200
        )
    else:
        return Response({
            'error': 'Invalid user type'
            },
            status=400
        )


@api_view(['POST'])
@permission_classes([IsSchoolPermission, RequiredProfileCompletionPermission(required_level=50)])
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