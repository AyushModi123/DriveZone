from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from base.utils import activation_token_manager, send_activation_mail
from .serializers import UserSerializer
from base.models import Instructor, Learner


User = get_user_model()

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save(is_active=False)
        user_type = request.data.get('user_type', None)
        if user_type == 'instructor':
            instructor = Instructor.objects.create(user=user)
        elif user_type == 'learner':
            learner = Learner.objects.create(user=user)
        else:
            return Response({'msg': 'Invalid user type'}, status=400)
        send_activation_mail(request, user)
        return Response({
            'user': UserSerializer(user, context={'request': request}).data,
            'message': 'User created successfully. Please activate your account by clicking on the link we sent to your email.'
        }, status=201)
    return Response(serializer.errors, status=400)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None:
        if activation_token_manager.check_token(user, token):
            if user.is_active:
                Response("Account is already activated", status=400)
            else:
                user.is_active = True
                user.save()
                return Response("Account Activated Successfully", status=200)
    return Response("Invalid Activation", status=400)


@api_view(['GET'])
def check_api(request):
    return Response("Working")