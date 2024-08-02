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
        permission_classes = [BlockInstructorPermission, RequiredProfileCompletionPermission(required_level=100)]
        if self.request.method not in ('list', 'retrieve'):
            permission_classes+=[IsLearnerPermission]
        return [permission() for permission in permission_classes]

    def list(self, request):
        current_user = request.user
        limit = request.GET.get("limit", 10)
        try:
            limit = int(limit)
        except (TypeError, ValueError):
            return Response({"message": "Invalid limit"}, status=400)

        if current_user.is_school:
            reviews = Review.objects.filter(school=current_user.school)[:limit]
            return Response({'reviews': OutReviewSerializer(reviews, many=True).data}, status=200)
        elif current_user.is_learner:
            school_id = request.GET.get("school_id", None)
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
        current_user = request.user
        school_id = request.GET.get("school_id", None)
        review_id = pk

        if current_user.is_school:                        
                try:
                    review = Review.objects.get(school=current_user.school, id=review_id)
                    return Response({'review': OutReviewSerializer(review, many=False).data}, status=200)
                except Review.DoesNotExist as e:
                    logger.info("Invalid Review id")
                    return Response({"message": "Invalid Review id"}, status=400)
        elif current_user.is_learner:
            try:
                school_id = int(school_id)
            except (TypeError, ValueError):
                return Response({"message": "Invalid School id"}, status=400)
            try:                
                review = Review.objects.get(school=school_id, id=review_id)
                return Response({'review': OutReviewSerializer(review, many=False).data}, status=200)
            except Review.DoesNotExist:
                logger.info("Invalid Review id")
                return Response({"message": "Invalid Review id"}, status=400)                
