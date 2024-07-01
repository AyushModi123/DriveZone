from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils.crypto import get_random_string
from drf_yasg.utils import swagger_auto_schema
from base.permissions import RequiredProfileCompletionPermission, IsSchoolPermission, BlockInstructorPermission, BlockSchoolPermission, IsNotAuthenticated
from firebase_utils import FirebaseUploadImage
from base.utils import activation_token_manager, send_activation_mail, send_instructor_login_details

from base.choices import RoleChoices
from .serializers import LearnerSerializer, SchoolSerializer, OutLearnerSerializer, OutSchoolSerializer,\
      OutInstructorSerializer, UserSerializer, OutUserSerializer, LicenseInformationSerializer, \
      OutShortInstructorSerializer, InstructorSerializer
from base.models import Instructor, Learner, ProfileCompletionLevelChoices

User = get_user_model()

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


@swagger_auto_schema(
    method='post',
    request_body=UserSerializer,    
)
@api_view(['POST'])
@authentication_classes([])
@permission_classes([IsNotAuthenticated])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save(is_active=False)        
        res = send_activation_mail(request, user)
        if res:
            return Response({
                'user': OutUserSerializer(user, context={'request': request}).data,
                'message': 'User created successfully. Please activate your account by clicking on the link we sent to your email.'
            }, status=201)
        else:
            return Response({"error": "Could not send activation email. Try Again"}, status=500)
    return Response(serializer.errors, status=400)

@swagger_auto_schema(
    method='post',
    request_body=SchoolSerializer,    
)
@api_view(['POST'])
#IsAuth & IsActive
def create_school(request):
    current_user = request.user
    if request.user.is_school:
        return Response({"message": "School already created"}, 200)
    if current_user.role == RoleChoices.SCHOOL:
        serializer = SchoolSerializer(data=request.data)
        if serializer.is_valid():
            school = serializer.save(user=current_user)
            image_file = request.FILES.get('image', None)
            if image_file is not None:
                img_url = FirebaseUploadImage.upload_image(image_file, 'profiles')
                school.image_url = img_url
                school.save()
            return Response({
                'user': SchoolSerializer(school, context={'request': request}).data,
                'message': 'School created successfully.'
            }, status=201)
        return Response(serializer.errors, status=400)
    else:
        return Response({"error": "Role Mismatch"}, status=400)

@swagger_auto_schema(
    method='post',
    request_body=LearnerSerializer,    
)
@api_view(['POST'])
#IsAuth & IsActive
def create_learner(request):
    current_user = request.user
    if current_user.role == RoleChoices.LEARNER:
        serializer = LearnerSerializer(data=request.data)
        if serializer.is_valid():
            school = serializer.save(user=request.user)                        
            image_file = request.FILES.get('image', None)
            if image_file:
                img_url = FirebaseUploadImage.upload_image(image_file, 'profiles')
                school.image_url = img_url
                school.save()
            return Response({
                'user': LearnerSerializer(school, context={'request': request}).data,
                'message': 'Learner created successfully.'
            }, status=201)
        return Response(serializer.errors, status=400)
    else:
        return Response({"error": "Role Mismatch"}, status=400)

@api_view(['POST'])
def upload_image(request):
    current_user = request.user
    image_file = request.FILES.get('image', None)    
    current_user_role_model = current_user.get_role_model
    if image_file:
        img_url = FirebaseUploadImage.upload_image(image_file, 'profiles')
        current_user_role_model.image_url = img_url
        current_user_role_model.save()
        return Response({'message': 'Image Uploaded', 'image_url': img_url}, status=201)
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
        return Response({'role': current_user.role}, status=200)

@swagger_auto_schema(
    method='post',
    request_body=LicenseInformationSerializer,    
)
@api_view(['POST'])
@permission_classes([BlockSchoolPermission])
def upload_license(request):
    current_user = request.user
    image_file = request.FILES.get('image', None)
    serializer = LicenseInformationSerializer(data=request.data)    
    if image_file:
        if serializer.is_valid():
            img_url = FirebaseUploadImage.upload_image(image_file, 'licenses')
            serializer.save(image_url=img_url, user=current_user)
            return Response({'message': 'License uploaded successfully', 'image_url': img_url}, status=201)
        else:
            return Response(serializer.errors, status=400)
    else:
        return Response({'error': 'Invalid Image File'}, status=400)
    
@swagger_auto_schema()
class InstructorView(APIView):
    permission_classes = [IsSchoolPermission, RequiredProfileCompletionPermission(required_level=50)]

    def get(self, request):
        current_user = request.user
        instructor_id = request.GET.get("id", None)
        if instructor_id is not None:
            try:
                instructor_id = int(instructor_id)
            except (TypeError, ValueError):
                return Response({"message": "Invalid Instructor id"}, status=400)
            try:
                instructor = Instructor.objects.get(id=instructor_id, school=current_user.school)
            except Instructor.DoesNotExist:
                return Response({'error': 'Invalid Instructor ID'}, status=400)
            return Response({'instructor': OutInstructorSerializer(instructor, many=False).data}, status=200)
        else:
            q = request.GET.get("q", "")
            instructors = Instructor.objects.filter(
                Q(school=current_user.school) &
                (
                    Q(full_name__icontains=q) | 
                    Q(location__icontains=q) |
                    Q(experience__iexact=q) |
                    Q(preferred_language__iexact=q)
                )
            )
            return Response({'instructors': OutShortInstructorSerializer(instructors, many=True).data}, status=200)

    @swagger_auto_schema(request_body=InstructorSerializer)
    def post(self, request):
        current_user = request.user
        serializer = InstructorSerializer(data=request.data)
        if serializer.is_valid():
            random_password = get_random_string(length=12)
            instructor = serializer.save(is_active=False, password=random_password, school=current_user.school)
            image_file = request.FILES.get('image', None)
            if image_file is not None:
                img_url = FirebaseUploadImage.upload_image(image_file, 'profiles')
                instructor.image_url = img_url
                instructor.save()
            send_activation_mail(request, instructor.user)
            send_instructor_login_details(request, instructor.user, current_user.school, random_password)
            return Response({
            'user': OutShortInstructorSerializer(instructor, context={'request': request}).data,
            'message': 'Instructor created successfully. Account will be activated once the instructor clicks on the link sent to their email'
        }, status=201)
        return Response(serializer.errors, status=400)



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