from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import BookingSerializer
from booking.models import Booking

@authentication_classes(JWTAuthentication)
@permission_classes(IsAuthenticated)
@api_view(['GET'])
def get_bookings(request):
    if request.user.is_authenticated:
        user = request.user
        if hasattr(user, 'instructor'):
            bookings = Booking.objects.get(instructor=user.instructor)
            return BookingSerializer(bookings, many=True)
        else:
            bookings = Booking.objects.get(instructor=user.learner)
            return BookingSerializer(bookings, many=True)
    else:
        return Response({'msg': 'User not authenticated'}, status=401)
    
@authentication_classes(JWTAuthentication)
@permission_classes(IsAuthenticated)
@api_view(['POST'])
def create_booking(request):
    if request.user.is_authenticated:
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
    else:
        return Response({'error': 'User not authenticated'}, status=401)
