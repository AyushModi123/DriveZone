from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from base.permissions import IsInstructorPermission, IsLearnerPermission
from base.models import User
from vehicle.models import Vehicle
from .serializers import InstructorVehicleSerializer, LearnerVehicleSerializer

@api_view(['POST'])
@permission_classes([IsInstructorPermission])
def create_vehicle(request):
    serializer = InstructorVehicleSerializer(data=request.data)
    if serializer.is_valid():
        vehicle = serializer.save()
        return Response('Vehicle Saved', status=201)
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
