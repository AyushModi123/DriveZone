import logging
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers
from drf_yasg.utils import swagger_auto_schema
from project_cemphris.permissions import IsSchoolPermission, IsLearnerPermission, RequiredProfileCompletionPermission, BlockInstructorPermission
from base.models import School, ProfileCompletionLevelChoices
from vehicle.models import Vehicle
from .serializers import VehicleSerializer, OutVehicleSerializer, ImageUploadSerializer
from firebase_utils import FirebaseUploadImage

logger = logging.getLogger(__file__)

@swagger_auto_schema()
class VehicleViewSet(viewsets.ViewSet):    

    def get_permissions(self):
        permission_classes = []
        if self.action not in {'list', 'retrieve'}:
            permission_classes.extend([IsSchoolPermission, RequiredProfileCompletionPermission(required_level=50)])
        return [permission() for permission in permission_classes]
    
    # @method_decorator(cache_page(settings.CACHE_TTL))    
    @swagger_auto_schema()
    def list(self, request):   
        school_id = request.GET.get("school_id", None) 
        try:
            school_id = int(school_id)
            school = School.objects.get(pk=school_id)
        except (TypeError, ValueError, School.DoesNotExist) as e:
            logger.exception(e)
            return Response({"message": "Invalid School id"}, status=400)        

        vehicles = Vehicle.objects.filter(
            Q(school=school)            
        )
        paginator = PageNumberPagination()
        page = paginator.paginate_queryset(vehicles, request)

        if page is not None:
            serializer = OutVehicleSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        # If pagination is not applied(for compatibility)
        return Response({'vehicles': OutVehicleSerializer(vehicles, many=True).data}, status=200)

    
    @swagger_auto_schema()
    def retrieve(self, request, pk=None):         
        try:
            vehicle = Vehicle.objects.get(id=pk)
        except Vehicle.DoesNotExist:
            return Response({"error": "Invalid Vehicle Id"}, status=400)
        return Response({"vehicle": OutVehicleSerializer(vehicle, many=False)}, status=200)

    @swagger_auto_schema(request_body=VehicleSerializer)
    def create(self, request):
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
        
    @swagger_auto_schema()
    def update(self, request, pk=None):
        current_user = request.user
        try:                
            vehicle = Vehicle.objects.get(id=pk, school=current_user.school)            
        except Vehicle.DoesNotExist as e:
            logger.exception(e)
            return Response({"error": "Vehicle not found"}, status=404)
        serializer = VehicleSerializer(instance=vehicle, data=request.data)
        if serializer.is_valid():
            vehicle = serializer.save()
            return Response(status=204)
        return Response(serializer.errors, status=400)
        

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