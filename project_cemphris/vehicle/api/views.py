from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from base.permissions import IsSchoolPermission, IsLearnerPermission, RequiredProfileCompletionPermission, BlockInstructorPermission
from base.models import User, ProfileCompletionLevelChoices
from vehicle.models import Vehicle
from .serializers import VehicleSerializer, OutVehicleSerializer
from firebase_utils import FirebaseUploadImage



class VehicleView(APIView):
    permission_classes = [IsSchoolPermission, RequiredProfileCompletionPermission(required_level=50)]

    def get(self, request):
        current_user = request.user
        vehicle_id = request.GET.get("id", None)        
        if vehicle_id is None:
            q = request.GET.get("q", "")
            vehicles = Vehicle.objects.filter(
                Q(school=current_user.school) &
                (
                    Q(model__icontains=q) | 
                    Q(license_no__icontains=q) |
                    Q(make__icontains=q) |
                    Q(type__icontains=q)
                )
            )
            return Response({'vehicles': OutVehicleSerializer(vehicles, many=True).data}, status=200)
        else:
            try:
                vehicle = Vehicle.objects.get(id=vehicle_id, school=current_user.school)
            except Vehicle.DoesNotExist:
                return Response({"error": "Invalid Vehicle Id"}, status=400)
            return Response({"vehicle": OutVehicleSerializer(vehicle, many=False)}, status=200)        

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
                return Response({'message': 'Vehicle Saved', 'vehicle_id': vehicle.id, 'image_url': img_url}, status=201)
            else:
                return Response(serializer.errors, status=400)
        else:
            return Response({'error': 'Invalid Image File'}, status=400)

# @api_view(['GET'])
# def get_vehicle(request):
#     """get vehicle by id"""
#     current_user = request.user
#     vehicle_id = request.GET.get('id', None)
#     try:
#         vehicle = Vehicle.objects.get(id=vehicle_id)
#     except Vehicle.DoesNotExist:
#         return Response({
#             'error': 'Vehicle Not Found'
#         }, status=404
#     )
#     if current_user.is_learner:                    
#             return Response({
#                 'vehicle': 
#                 }, status=200
#             )
#     elif current_user.is_school:        
#         return Response({
#             'vehicle': 
#             },
#             status=200
#         )
#     else:
#         return Response({
#             'error': 'Invalid user type'
#             },
#             status=400
#         )


@api_view(['PUT'])
@permission_classes([IsSchoolPermission, RequiredProfileCompletionPermission(required_level=50)])
def upload_image(request):
    image_file = request.FILES.get('image', None)
    vehicle_id = request.data.get('id', None)    
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