from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from base.permissions import IsLearnerPermission, RequiredProfileCompletionPermission
from .serializers import BookingSerializer
from booking.models import Booking
from base.models import Learner, Instructor, ProfileCompletionLevelChoices

@api_view(['GET'])
def get_bookings(request):    
    user = request.user
    try:
        instructor = user.instructor
        bookings = Booking.objects.filter(instructor=instructor)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)
    except Instructor.DoesNotExist:
        try:
            learner = user.learner
            bookings = Booking.objects.filter(learner=learner)
            serializer = BookingSerializer(bookings, many=True)
            return Response(serializer.data)
        except Learner.DoesNotExist:
            return Response({'msg': 'User has no associated Learner or Instructor'}, status=404)

@swagger_auto_schema(
    method='post',
    request_body=BookingSerializer,    
)
@api_view(['POST'])
@permission_classes([IsLearnerPermission, RequiredProfileCompletionPermission(required_level=100)])
def create_booking(request):
    user = request.user
    if hasattr(user, 'learner'):
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            booking = serializer.save(learner=user.learner)
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)
    else:
        return Response({'msg': 'Not Found'}, status=404)
