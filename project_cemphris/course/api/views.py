import logging
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import viewsets
from drf_yasg.utils import swagger_auto_schema
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers
from django.db.models import Q
from project_cemphris.permissions import IsSchoolPermission, IsLearnerPermission, RequiredProfileCompletionPermission, BlockInstructorPermission
from base.models import User, ProfileCompletionLevelChoices
from course.models import Course, EnrollCourse
from .serializers import CourseSerializer, OutSchoolCourseSerializer, OutCourseSerializer, OutShortCourseSerializer, OutShortSchoolCourseSerializer, EnrollCourseSerializer, OutLearnerEnrollCourseSerializer, OutEnrollCourseSerializer
from firebase_utils import FirebaseUploadImage

logger = logging.getLogger(__file__)

@swagger_auto_schema()
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
        
        if current_user and current_user.is_authenticated and current_user.is_school:
            courses = Course.objects.filter(school=current_user.school)
            return Response({"courses": OutShortSchoolCourseSerializer(courses, many=True).data}, status=200)
        else:
            school_id = request.GET.get('school_id', None)
            if school_id is not None:
                try:
                    school_id = int(school_id)
                except (TypeError, ValueError):
                    return Response({"message": "Invalid School id"}, status=400)
                courses = Course.objects.filter(school=school_id, is_active=True)
                return Response({"courses": OutShortCourseSerializer(courses, many=True).data}, status=200)
            else:
                return Response({"message": "Invalid School id"}, status=400)

    def create(self, request):
        serializer = CourseSerializer(data=request.data)
        current_user = request.user
        if serializer.is_valid():
            course = serializer.save(school=current_user.school)
            return Response({"message": "Course created", "id": course.id}, status=201)
        return Response(serializer.errors, status=400)
    
    def retrieve(self, request, pk=None):
        current_user = request.user
        try:
            if current_user and current_user.is_authenticated and current_user.is_school:            
                course = Course.objects.get(pk=pk, school=current_user.school)            
                return Response({"course": OutSchoolCourseSerializer(course, many=False).data}, status=200)
            else:            
                course = Course.objects.get(pk=pk, is_active=True)
                return Response({"course": OutCourseSerializer(course, many=False).data}, status=200)
        except Course.DoesNotExist:
            return Response({"error": "Course not found"}, status=404)

    def update(self, request, pk=None):
        current_user = request.user
        try:
            course = Course.objects.get(pk=pk, school=current_user.school)
        except Course.DoesNotExist:
            return Response({"error": "Course not found"}, status=404)
        serializer = CourseSerializer(instance=course, data=request.data)
        if serializer.is_valid():
            course = serializer.save()
            return Response(status=204)
        return Response(serializer.errors, status=400)

    def partial_update(self, request, pk=None):
        current_user = request.user
        try:
            course = Course.objects.get(pk=pk, school=current_user.school)
        except Course.DoesNotExist:
            return Response({"error": "Course not found"}, status=404)
        serializer = CourseSerializer(instance=course, data=request.data, partial=True)
        if serializer.is_valid():
            course = serializer.save()
            return Response(status=204)
        return Response(serializer.errors, status=400)

    # def destroy(self, request, pk=None):
    #     current_user = request.user
    #     try:
    #         course = Course.objects.get(pk=pk, school=current_user.school)
    #     except Course.DoesNotExist:
    #         return Response({"error": "Course not found"}, status=404)
    #     course.delete(keep_parents=True)
    #     return Response({"message": "Course deleted successfully"}, status=204)
    
swagger_auto_schema(
    method='POST',
    request_body=EnrollCourseSerializer
)
@api_view(["POST"])
@permission_classes([IsSchoolPermission])
def assign_instructor(request, pk=None):
    current_user = request.user
    try:
        enroll_course = EnrollCourse.objects.select_related("course").get(
            Q(pk=pk) &
            Q(course__school=current_user.school)
        )
    except EnrollCourse.DoesNotExist:
        return Response({"error": "Enrollment Not Found"}, status=404)
    serializer = EnrollCourseSerializer(instance=enroll_course, data=request.data)
    if serializer.is_valid():
        learner = serializer.validated_data['learner']
        course = serializer.validated_data['course']
        if not (enroll_course.learner == learner and enroll_course.course == course):
            return Response({"error": "Invalid course or learner id"}, status=404)        
        enroll_course = serializer.save()
        return Response({"message": "Instructor Assigned Successfully"}, status=200)
    return Response(serializer.errors, status=400)

@swagger_auto_schema(
        method='GET'
)
@api_view(["GET"])
@permission_classes([BlockInstructorPermission])
def get_enrollment(request):
    current_user = request.user
    if current_user.is_learner:
        try:
            enroll_course = EnrollCourse.objects.get(learner=current_user.learner)
            return Response({"enrollment": OutLearnerEnrollCourseSerializer(enroll_course, many=False).data}, status=200)
        except EnrollCourse.DoesNotExist:
            return Response({"error": "Not Enrolled"}, status=404)
    elif current_user.is_school:        
        courses = Course.objects.filter(school=current_user.school, is_active=True)
        response_data = []
        for course in courses:
            enrolled_entities = course.get_enrolled()
            if enrolled_entities:
                response_data.extend(OutEnrollCourseSerializer(enrolled_entities, many=True).data)
        return Response({"enrollments": response_data}, status=200)
    else:
        Response({'error': 'Permission Denied'}, status=403)
