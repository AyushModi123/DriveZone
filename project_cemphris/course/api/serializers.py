from rest_framework import serializers
from course.models import Course, EnrollCourse

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('course_content',)

class OutCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('school', 'course_content', 'id')

class EnrollCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnrollCourse
        fields = ('learner', 'course', 'instructor')    