from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers
from drf_yasg.utils import swagger_auto_schema
from project_cemphris.permissions import IsSchoolPermission, IsLearnerPermission, RequiredProfileCompletionPermission, BlockInstructorPermission
from base.models import User, ProfileCompletionLevelChoices
from vehicle.models import Vehicle
from .serializers import VehicleSerializer, OutVehicleSerializer, ImageUploadSerializer
from firebase_utils import FirebaseUploadImage


@swagger_auto_schema()
class VehicleView(APIView):
    permission_classes = [IsSchoolPermission, RequiredProfileCompletionPermission(required_level=50)]
    @method_decorator(cache_page(settings.CACHE_TTL))
    @method_decorator(vary_on_headers("Authorization"))
    @swagger_auto_schema()
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
                vehicle_id = int(vehicle_id)
            except (TypeError, ValueError):
                return Response({"message": "Invalid Vehicle id"}, status=400)
            try:
                vehicle = Vehicle.objects.get(id=vehicle_id, school=current_user.school)
            except Vehicle.DoesNotExist:
                return Response({"error": "Invalid Vehicle Id"}, status=400)
            return Response({"vehicle": OutVehicleSerializer(vehicle, many=False)}, status=200)

    @swagger_auto_schema(request_body=VehicleSerializer)
    def post(self, request):
        serializer = VehicleSerializer(data=request.data)
        image_data = request.FILES.get("image", None)
        if serializer.is_valid():
            image_url = ""
            if image_data is not None:
                image_serializer = ImageUploadSerializer(data=request.FILES)
                if image_serializer.is_valid():
                    image_file = image_serializer.validated_data.get('image')
                    image_url = FirebaseUploadImage.upload_image(image_file, 'vehicles')
                else:
                    return Response(image_serializer.errors, status=400)
            vehicle = serializer.save(
                image_url=image_url, 
                school=request.user.school
            )
            return Response({'message': 'Vehicle Saved', 'vehicle_id': vehicle.id, 'image_url': image_url}, status=201)
        else:
            return Response(serializer.errors, status=400)

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
    serializer = ImageUploadSerializer(data=request.FILES)
    vehicle_id = request.data.get('id', None)
    try:
        vehicle_id = int(vehicle_id)
    except (TypeError, ValueError):
        return Response({"error": "Invalid vehicle id"}, status=400)
    if serializer.is_valid():        
            try:            
                vehicle = Vehicle.objects.get(id=vehicle_id)
            except Vehicle.DoesNotExist:
                return Response({'error': 'Invalid Vehicle Id'}, status=400)
            image_file = serializer.validated_data.get('image')
            image_url = FirebaseUploadImage.upload_image(image_file, 'vehicles')
            vehicle.image_url = image_url
            vehicle.save()
            return Response({'message': 'Image Uploaded', 'vehicle_id': vehicle.id, 'image_url': image_url}, status=200)
    else:
        return Response({'error': 'Invalid Image File'}, status=400)