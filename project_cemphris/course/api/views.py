from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import viewsets
from drf_yasg.utils import swagger_auto_schema
from base.permissions import IsSchoolPermission, IsLearnerPermission, RequiredProfileCompletionPermission, BlockInstructorPermission
from base.models import User, ProfileCompletionLevelChoices
from course.models import Course
from .serializers import CourseSerializer, OutCourseSerializer
from firebase_utils import FirebaseUploadImage

class CourseViewSet(viewsets.ViewSet):    

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        common_permission_classes = []
        if self.action in ('update', 'create', 'partial_update', 'destroy'):
            permission_classes = common_permission_classes + [IsSchoolPermission]
        else:
            permission_classes = common_permission_classes
        return [permission() for permission in permission_classes]
    
    def list(self, request):
        current_user = request.user
        
        if current_user.is_authenticated and current_user.is_school:
            courses = Course.objects.filter(school=current_user.school)
            return Response({"courses": OutCourseSerializer(courses, many=True).data}, status=200)
        else:
            school_id = request.GET.get('school_id', None)
            if school_id is not None:
                try:
                    school_id = int(school_id)
                except (TypeError, ValueError):
                    return Response({"message": "Invalid School id"}, status=400)
                courses = Course.objects.filter(school=school_id)
                return Response({"courses": OutCourseSerializer(courses, many=True).data}, status=200)
            else:
                return Response({"message": "Invalid School id"}, status=400)

    def create(self, request):
        serializer = CourseSerializer(data=request.data)
        current_user = request.user
        if serializer.is_valid():
            course = serializer.save(school=current_user.school)
            return Response({"message": "Course created", "id": course.id}, status=201)
        return Response(serializer.errors, status=400)

    # def retrieve(self, request, pk=None):
    #     pass

    # def update(self, request, pk=None):
    #     pass

    # def partial_update(self, request, pk=None):
    #     pass

    # def destroy(self, request, pk=None):
    #     pass