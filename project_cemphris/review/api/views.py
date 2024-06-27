from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from base.permissions import RequiredProfileCompletionPermission, BlockInstructorPermission
from .serializers import OutReviewSerializer
from review.models import Review

@swagger_auto_schema()
class ReviewView(APIView):
    permission_classes = [BlockInstructorPermission, RequiredProfileCompletionPermission(required_level=100)]

    def get(self, request):
        current_user = request.user
        school_id = request.GET.get("school_id", None)

        try:
            school_id = int(school_id)
        except (TypeError, ValueError):
            return Response({"message": "Invalid School id"}, status=400)
        
        if current_user.is_school:            
            if not (current_user.school.id == school_id):
                return Response({"message": "Access Denied"}, status=403)
                        
        review_id = request.GET.get("review_id", None)

        if review_id is None:
            reviews = Review.objects.filter(school=school_id)
            return Response({'reviews': OutReviewSerializer(reviews, many=True).data}, status=200)
        else:
            try:
                review_id = int(review_id)            
                review = Review.objects.get(school=school_id, id=review_id)
            except (TypeError, ValueError, Review.DoesNotExist):
                return Response({"message": "Invalid Review id"}, status=400)            
            
            return Response({'review': OutReviewSerializer(review, many=False).data}, status=200)        


