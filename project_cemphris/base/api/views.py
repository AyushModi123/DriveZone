import logging
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from django.conf import settings
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils.crypto import get_random_string
from drf_yasg.utils import swagger_auto_schema
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers
from base.permissions import RequiredProfileCompletionPermission, IsSchoolPermission, BlockInstructorPermission, \
    BlockSchoolPermission, IsNotAuthenticated, IsLearnerPermission
from firebase_utils import FirebaseUploadImage
from base.utils import activation_token_manager, password_reset_token_manager, send_activation_mail, \
    send_instructor_login_details, send_reset_password_email, send_password_reset_email

from base.constants import MAX_ACTIVATION_MAIL_SENT_COUNT
from base.choices import RoleChoices
from .serializers import LearnerSerializer, SchoolSerializer, OutLearnerSerializer, OutSchoolSerializer,\
      OutInstructorSerializer, UserSerializer, OutUserSerializer, LicenseInformationSerializer, \
      OutShortInstructorSerializer, InstructorSerializer, OutShortSchoolSerializer, OutVeryShortSchoolSerializer, \
      EmailSerializer, ResetPasswordSerializer, ImageUploadSerializer
from base.models import Instructor, School, Learner, ProfileCompletionLevelChoices, ActivationMailHistory

logger = logging.getLogger(__file__)

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

@swagger_auto_schema()
class PasswordReset(APIView):
    permission_classes = []
    authentication_classes = []

    def get(request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None:
            if password_reset_token_manager.check_token(user, token):
                return Response({"message": "Validated"}, status=200)
        return Response({'error': 'Invalid Link'}, status=400)

    @swagger_auto_schema(request_body=ResetPasswordSerializer)
    def post(request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None:
            if password_reset_token_manager.check_token(user, token):
                serializer = ResetPasswordSerializer(data=request.data)
                if serializer.is_valid():
                    user.set_password(serializer.validated_data.get('password'))
                    user.save()
                    return Response({'message': 'Password updated'}, status=200)
                return Response(serializer.errors, status=400)
        return Response({'error': 'Invalid Link'}, status=400)


@swagger_auto_schema(
    method='post',
    request_body=EmailSerializer,    
)
@api_view(['POST'])
@permission_classes([])
def password_reset(request):
    if request.user.is_authenticated:
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            request.user.set_password(serializer.validated_data.get('password'))
            request.user.save()
            send_password_reset_email(request, user)
            return Response({'message': 'Password updated'}, status=200)
        return Response(serializer.errors, status=400)
    else:
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get("email", None)
            try:
                user = User.objects.get(email=email)
                send_reset_password_email(request, user)
            except User.DoesNotExist:
                logger.info("Email not found for password reset request")
            return Response({'message': 'We have sent password reset link to your email.'}, status=200)
        return Response(serializer.errors, status=400)


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
        send_activation_mail(request, user)
        return Response({
            'user': OutUserSerializer(user, context={'request': request}).data,
            'message': 'User created successfully. Please activate your account by clicking on the link we sent to your email.'
        }, status=201)
    return Response(serializer.errors, status=400)

@swagger_auto_schema(
    method='post',
    request_body=EmailSerializer,    
)
@api_view(['POST'])
@permission_classes([])
def resend_activation_mail(request):
    serializer = EmailSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data.get("email")
        try:
            user = User.objects.get(email=email)
            if user.is_active:
                return Response({"message": "User already activated"}, status=200)
            act_hist, _ = ActivationMailHistory.objects.get_or_create(email=email)
            if act_hist.sent_count >= MAX_ACTIVATION_MAIL_SENT_COUNT:
                return Response({
                    'message': 'Max Retries Reached'
                }, status=403)
            send_activation_mail(request, user)
            act_hist.sent_count+=1
            act_hist.save()
        except User.DoesNotExist as e:
            logger.exception(e)
        return Response({                
            'message': 'Please activate your account by clicking on the link we sent to your email.'
        }, status=200)
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
        image_data = request.FILES.get("image", None)
        if serializer.is_valid():
            image_url = ""
            if image_data is not None:
                image_serializer = ImageUploadSerializer(data=request.FILES)
                if image_serializer.is_valid():
                    image_file = image_serializer.validated_data.get('image')
                    image_url = FirebaseUploadImage.upload_image(image_file, 'profiles')                    
                else:
                    return Response(image_serializer.errors, status=400)            
            school = serializer.save(
                user=current_user, 
                image_url=image_url
            )
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
        image_data = request.FILES.get("image", None)
        if serializer.is_valid():
            image_url = ""
            if image_data is not None:   
                image_serializer = ImageUploadSerializer(data=request.FILES)
                if image_serializer.is_valid():
                    image_file = image_serializer.validated_data.get('image')         
                    image_url = FirebaseUploadImage.upload_image(image_file, 'profiles')
                else:
                    return Response(image_serializer.errors, status=400)
            learner = serializer.save(
                user=request.user, 
                image_url=image_url
                )
            return Response({
                'user': LearnerSerializer(learner, context={'request': request}).data,
                'message': 'Learner created successfully.'
            }, status=201)
        return Response(serializer.errors, status=400)
    else:
        return Response({"error": "Role Mismatch"}, status=400)

@swagger_auto_schema(
    method='patch',
    request_body=LearnerSerializer,    
)
@api_view(['PATCH'])
@permission_classes([IsLearnerPermission])
def update_learner(request):
    current_user = request.user
    serializer = LearnerSerializer(current_user.learner, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"user": serializer.data}, status=200)
    return Response(serializer.errors, status=400)

@swagger_auto_schema(
    method='patch',
    request_body=SchoolSerializer,    
)
@api_view(['PATCH'])
@permission_classes([IsSchoolPermission])
def update_school(request):
    current_user = request.user
    serializer = SchoolSerializer(current_user.school, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"user": serializer.data}, status=200)
    return Response(serializer.errors, status=400)


@api_view(['PUT'])
def upload_image(request):
    current_user = request.user
    serializer = ImageUploadSerializer(data=request.FILES)
    current_user_role_model = current_user.get_role_model
    if serializer.is_valid():
        image_file = serializer.validated_data.get('image')
        image_url = FirebaseUploadImage.upload_image(image_file, 'profiles')
        current_user_role_model.image_url = image_url
        current_user_role_model.save()
        return Response({'message': 'Image Uploaded', 'image_url': image_url}, status=200)
    else:
        return Response({'error': 'Invalid Image File'}, status=400)
    

@cache_page(settings.CACHE_TTL)
@vary_on_headers("Authorization")
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
    serializer = LicenseInformationSerializer(data=request.data)
    image_data = request.FILES.get("image", None)    
    if serializer.is_valid():        
        image_url = ""
        if image_data is not None:
            image_serializer = ImageUploadSerializer(data=request.FILES)
            if image_serializer.is_valid():
                image_file = image_serializer.validated_data.get('image')
                image_url = FirebaseUploadImage.upload_image(image_file, 'licenses')
            else:
                return Response(image_serializer.errors, status=400)
        license = serializer.save(
            image_url=image_url, 
            user=current_user
            )
        return Response({'message': 'License uploaded successfully', 'image_url': image_url, 'license_id': license.pk}, status=201)
    else:
        return Response(serializer.errors, status=400)
    
@swagger_auto_schema()
class InstructorViewSet(viewsets.ViewSet):    
    def get_permissions(self):
        permission_classes = []
        if self.action not in {'list', 'retrieve'}:
            permission_classes.extend([IsSchoolPermission, RequiredProfileCompletionPermission(required_level=50)])
        return [permission() for permission in permission_classes]
    
    # @method_decorator(cache_page(settings.CACHE_TTL))
    def list(self, request):
        if request.user.is_authenticated and request.user.is_school:
            school = request.user.school
        else:
            school_id = request.GET.get("school_id", None)
            try:
                school_id = int(school_id)
                school = School.objects.get(pk=school_id)
            except (TypeError, ValueError, School.DoesNotExist):
                logger.info("Invalid School id")
                return Response({"message": "Invalid School id"}, status=400)        
        instructors = Instructor.objects.filter(
            Q(school=school)
        )
        paginator = PageNumberPagination()
        page = paginator.paginate_queryset(instructors, request)

        if page is not None:
            serializer = OutShortInstructorSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        # If pagination is not applied(for compatibility)
        return Response({'instructors': OutShortInstructorSerializer(instructors, many=True).data}, status=200)

    # @method_decorator(cache_page(settings.CACHE_TTL))
    def retrieve(self, request, pk=None):
        try:
            instructor = Instructor.objects.get(id=pk)
        except Instructor.DoesNotExist:
            return Response({'error': 'Invalid Instructor ID'}, status=400)
        return Response({'instructor': OutInstructorSerializer(instructor, many=False).data}, status=200)

    @swagger_auto_schema(request_body=InstructorSerializer)
    def create(self, request):
        current_user = request.user
        serializer = InstructorSerializer(data=request.data)
        image_data = request.FILES.get("image", None)
        if serializer.is_valid():
            image_url = ""
            if image_data is not None:
                image_serializer = ImageUploadSerializer(data=request.FILES)
                if image_serializer.is_valid():
                    image_file = image_serializer.validated_data.get('image')
                    image_url = FirebaseUploadImage.upload_image(image_file, 'profiles')
                else:
                    return Response(image_serializer.errors, status=400)
            random_password = get_random_string(length=12)
            instructor = serializer.save(is_active=False, password=random_password, school=current_user.school, image_url=image_url)
            send_activation_mail(request, instructor.user)
            send_instructor_login_details(request, instructor.user, current_user.school, random_password)
            return Response({
            'user': OutShortInstructorSerializer(instructor, context={'request': request}).data,
            'message': 'Instructor created successfully. Account will be activated once the instructor clicks on the link sent to their email'
                }, status=201)
        return Response(serializer.errors, status=400)

    def update(self, request, pk=None):
        current_user = request.user
        try:
            instructor = Instructor.objects.get(id=pk, school=current_user.school)
        except Instructor.DoesNotExist:
            return Response({'error': 'Invalid Instructor ID'}, status=400)
        serializer = InstructorSerializer(instance=instructor, data=request.data)
        if serializer.is_valid():
            instructor = serializer.save()
            return Response(status=204)
        return Response(serializer.errors, status=400)

    def partial_update(self, request, pk=None):     
        current_user = request.user   
        try:
            instructor = Instructor.objects.get(id=pk, school=current_user.school)
        except Instructor.DoesNotExist:
            return Response({'error': 'Invalid Instructor ID'}, status=400)
        serializer = InstructorSerializer(instance=instructor, data=request.data, partial=True)
        if serializer.is_valid():
            instructor = serializer.save()
            return Response(status=204)
        return Response(serializer.errors, status=400)

class SchoolViewSet(viewsets.ViewSet):
    permission_classes = []
    authentication_classes = []

    @method_decorator(cache_page(settings.CACHE_TTL))
    def list(self, request):
        query_location: str = request.GET.get("location", "Pune")
        query_name: str = request.GET.get("name", "")
        schools = School.objects.filter(
            Q(location__icontains=query_location) &
            (
                Q(name__icontains=query_name)
            )
        )
        paginator = PageNumberPagination()
        page = paginator.paginate_queryset(schools, request)

        if page is not None:
            serializer = OutVeryShortSchoolSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        
        # If pagination is not applied(for compatibility)
        return Response({'schools': OutVeryShortSchoolSerializer(schools, many=True).data}, status=200)

    @method_decorator(cache_page(settings.CACHE_TTL))
    def retrieve(self, request, pk=None):
        query_location: str = request.GET.get("location", "Pune")
        try:
            school = School.objects.get(
                Q(pk=pk) &
                (
                    Q(location__icontains=query_location)
                )
            )
        except School.DoesNotExist:
            return Response({'error': "Invalid School Id"}, status=404)
        return Response({'school': OutShortSchoolSerializer(school, many=False).data}, status=200)

def check_api(request):
    print('REMOTE_ADDR--', request.META.get('REMOTE_ADDR', None))
    print('HTTP_X_REAL_IP--', request.META.get('HTTP_X_REAL_IP', None))
    print('HTTP_X_FORWARDED_FOR--', request.META.get('HTTP_X_FORWARDED_FOR', None))
    print(request.META)
    return Response("Working")
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
