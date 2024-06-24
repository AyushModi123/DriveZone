from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from base.permissions import RequiredProfileCompletionPermission, IsInstructorPermission
from firebase_utils import FirebaseUploadImage
from base.utils import activation_token_manager, send_activation_mail
from .serializers import LearnerSerializer, SchoolSerializer, OutLearnerSerializer, OutSchoolSerializer, OutInstructorSerializer, LicenseInformationSerializer
from base.models import Instructor, Learner, ProfileCompletionLevelChoices

User = get_user_model()

@swagger_auto_schema(
    method='post',
    request_body=LearnerSerializer,    
)
@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def signup(request):
    serializer = LearnerSerializer(data=request.data)
    if serializer.is_valid():
        learner = serializer.save(is_active=False)                            
        image_file = request.FILES.get('image', None)
        if image_file:
            img_url = FirebaseUploadImage.upload_image(image_file, 'profiles')
            learner.image_url = img_url
            learner.save()
        send_activation_mail(request, learner.user)
        return Response({
            'user': LearnerSerializer(learner, context={'request': request}).data,
            'message': 'User created successfully. Please activate your account by clicking on the link we sent to your email.'
        }, status=201)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def create_school(request):
    serializer = SchoolSerializer(data=request.data)
    if serializer.is_valid():
        school = serializer.save(is_active=False)                        
        image_file = request.FILES.get('image', None)
        if image_file:
            img_url = FirebaseUploadImage.upload_image(image_file, 'profiles')
            school.image_url = img_url
            school.save()
        send_activation_mail(request, school.user)
        return Response({
            'user': SchoolSerializer(school, context={'request': request}).data,
            'message': 'School created successfully. Please activate your account by clicking on the link we sent to your email.'
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

@api_view(['POST'])
@permission_classes([RequiredProfileCompletionPermission(required_level=ProfileCompletionLevelChoices.BASIC)])
def upload_image(request):
    current_user = request.user
    image_file = request.FILES.get('image', None)    
    if image_file:
        img_url = FirebaseUploadImage.upload_image(image_file, 'profiles')
        current_user.image_url = img_url
        current_user.save()
        return Response({'message': 'Image Uploaded', 'user_id': current_user.id}, status=200)
    else:
        return Response({'error': 'Invalid Image File'}, status=400)

@api_view(['GET'])
def get_user_details(request):
    current_user = request.user
    if current_user.is_learner:
        return Response(OutLearnerSerializer(current_user.learner).data, status=200)
    elif current_user.is_school:
        return Response(OutSchoolSerializer(current_user.school).data, status=200)
    elif current_user.is_instructor:
        return Response(OutInstructorSerializer(current_user.instructor).data, status=200)
    else:
        Response({'message': 'Invalid user type'}, status=400)
# @api_view(['PUT'])
# def update_details(request):
#     current_user = request.user
#     if request.user.is_learner:
#         serializer = LearnerDetailsSerializer(instance=request.user.learner, data=request.data)
#     elif request.user.is_instructor:
#         serializer = InstructorDetailsSerializer(instance=request.user.instructor, data=request.data)
#     else:
#         return Response({"message": "Invalid User"}, status=400)
#     if serializer.is_valid():
#         _ = serializer.save(user=current_user)
#         current_user.save()
#         return Response({"message": "Details Updated Successfully"}, status=200)
#     return Response(serializer.errors, status=400)

# @swagger_auto_schema(
#     method='put',
#     request_body=LicenseInformationSerializer,    
# )
# @api_view(['PUT'])
# def update_license(request):
#     current_user = request.user
#     license = None
#     if request.user.check_license:
#         license = request.user.license
#     serializer = LicenseInformationSerializer(instance=license, data=request.data)
#     if serializer.is_valid():
#         image_file = request.FILES.get('image', None)
#         img_url =''
#         if image_file:
#             img_url = FirebaseUploadImage.upload_image(image_file, 'licenses')
#         _ = serializer.save(
#             user=request.user,
#             image_url=img_url
#         )        
#         current_user.save()
#         return Response({"message": "Details Updated Successfully"}, status=200)
#     return Response(serializer.errors, status=400)

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def check_api(request):
    return Response("Working")