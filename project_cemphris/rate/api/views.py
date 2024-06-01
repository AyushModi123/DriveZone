from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from base.permissions import IsInstructorPermission, IsLearnerPermission
from base.models import User
from rate.models import Rating


@api_view(['POST'])
@permission_classes([IsLearnerPermission])
def rate_instructor(request):
    rating = request.GET.get('rating', None)
    instructor_username = request.GET.get('username', None)
    try:
        user = User.objects.get(username=instructor_username)
    except User.DoesNotExist:
        return Response({"error": "Instructor Not Found"}, status=404)
    if rating and type(rating, int):
        rate = Rating.objects.create(instructor=user.instructor, rating=rating)
        rate.save()
        return Response('Thank you for the rating', status=201)
    else:
        return Response({'error': 'Rating should be an integer'}, status=400)

@api_view(['GET'])
def get_rating(request):
    instructor_username = request.GET.get('username', None)
    try:
        user = User.objects.get(username=instructor_username)
    except User.DoesNotExist:
        return Response({"error": "Instructor Not Found"}, status=404)
    return Response({"rating": Rating.objects.get(instructor=user.instructor).rating}, status=200)


