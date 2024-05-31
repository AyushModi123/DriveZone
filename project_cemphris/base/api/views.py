from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from base.models import Instructor, Learner

User = get_user_model()

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        user_type = request.data.get('user_type', None)
        if user_type == 'instructor':
            instructor = Instructor.objects.create(user=user)
        elif user_type == 'learner':
            learner = Learner.objects.create(user=user)
        else:
            return Response({'msg': 'Invalid user type'}, status=400)

        return Response({
            'user': UserSerializer(user, context={'request': request}).data,
            'message': 'User created successfully.'
        }, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
def check_api(request):
    return Response("Working")