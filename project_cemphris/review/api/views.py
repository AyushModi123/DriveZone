import logging
from rest_framework.response import Response
# from rest_framework.views import APIView
from rest_framework import viewsets
from drf_yasg.utils import swagger_auto_schema
from project_cemphris.permissions import RequiredProfileCompletionPermission, BlockInstructorPermission, IsLearnerPermission
from .serializers import OutReviewSerializer, ReviewSerializer
from review.models import Review

logger = logging.getLogger(__file__)

@swagger_auto_schema()
class ReviewViewSet(viewsets.ViewSet):

    def get_permissions(self):
        permission_classes = []
        if self.action not in {'list', 'retrieve'}:
            permission_classes.extend([IsLearnerPermission, RequiredProfileCompletionPermission(required_level=100)])
        return [permission() for permission in permission_classes]
    
    def list(self, request):        
        school_id = request.GET.get("school_id", None)
        limit = request.GET.get("limit", 10)
        try:
            limit = int(limit)
        except (TypeError, ValueError):
            return Response({"message": "Invalid limit"}, status=400)        
        try:
            school_id = int(school_id)
        except (TypeError, ValueError):
            return Response({"message": "Invalid school_id"}, status=400)
        reviews = Review.objects.filter(school=school_id)[:limit]
        return Response({'reviews': OutReviewSerializer(reviews, many=True).data}, status=200)
        
    @swagger_auto_schema(request_body=ReviewSerializer)
    def create(self, request):
        current_user = request.user
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            review = serializer.save(learner=current_user.learner)
            return Response({"message": OutReviewSerializer(review).data}, status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):                
        try:                
            review = Review.objects.get(id=pk)
            return Response({'review': OutReviewSerializer(review, many=False).data}, status=200)
        except Review.DoesNotExist as e:
            logger.exception(e)
            return Response({"message": "Invalid Review id"}, status=400)
    
    def update(self, request, pk=None):
        current_user = request.user
        try:                
            review = Review.objects.get(id=pk, learner=current_user.learner)            
        except Review.DoesNotExist as e:
            logger.exception(e)
            return Response({"message": "Invalid Review id"}, status=400)
        serializer = ReviewSerializer(instance=review, data=request.data)
        if serializer.is_valid():
            review = serializer.save()
            return Response(status=204)
        return Response(serializer.errors, status=400)

