from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from base.permissions import RequiredProfileCompletionPermission, BlockInstructorPermission, IsLearnerPermission
from .serializers import OutReviewSerializer, ReviewSerializer
from review.models import Review

@swagger_auto_schema()
class ReviewView(APIView):

    def get_permissions(self):
        permission_classes = [BlockInstructorPermission, RequiredProfileCompletionPermission(required_level=100)]
        if self.request.method not in ('GET', ):
            permission_classes+=[IsLearnerPermission]
        return [permission() for permission in permission_classes]

    def get(self, request):
        current_user = request.user
        school_id = request.GET.get("school_id", None)
        review_id = request.GET.get("review_id", None)

        if current_user.is_school:
            if review_id is None:
                reviews = Review.objects.filter(school=current_user.school)
                return Response({'reviews': OutReviewSerializer(reviews, many=True).data}, status=200)
            else:
                try:
                    review_id = int(review_id)
                    review = Review.objects.get(school=current_user.school, id=review_id)
                    return Response({'review': OutReviewSerializer(review, many=False).data}, status=200)
                except (TypeError, ValueError, Review.DoesNotExist):
                    return Response({"message": "Invalid Review id"}, status=400)
        else:
            try:
                school_id = int(school_id)
            except (TypeError, ValueError):
                return Response({"message": "Invalid School id"}, status=400)
            if review_id is None:
                reviews = Review.objects.filter(school=school_id)
                return Response({'reviews': OutReviewSerializer(reviews, many=True).data}, status=200)
            else:
                try:
                    review_id = int(review_id)
                    review = Review.objects.get(school=school_id, id=review_id)
                    return Response({'review': OutReviewSerializer(review, many=False).data}, status=200)
                except (TypeError, ValueError, Review.DoesNotExist):
                    return Response({"message": "Invalid Review id"}, status=400)                

    @swagger_auto_schema(request_body=ReviewSerializer)
    def post(self, request):
        current_user = request.user
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            review = serializer.save(learner=current_user.learner)
            return Response({"message": OutReviewSerializer(review).data}, status=201)
        return Response(serializer.errors, status=400)
