from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from firebase_utils import FirebaseUploadImage
from base.utils import send_activation_mail
from .serializers import SchoolSerializer
from school.models import School
from base.api.serializers import UserSerializer

@api_view(['POST'])
def create_school(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save(is_active=False)                
        school = School.objects.create(user=user)
        school.save()        
        image_file = request.FILES.get('image', None)
        if image_file:
            img_url = FirebaseUploadImage.upload_image(image_file, 'profiles')
            user.image_url = img_url
            user.save()
        send_activation_mail(request, user)
        return Response({
            'user': UserSerializer(user, context={'request': request}).data,
            'message': 'School created successfully. Please activate your account by clicking on the link we sent to your email.'
        }, status=201)
    return Response(serializer.errors, status=400)


@api_view(['POST'])
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