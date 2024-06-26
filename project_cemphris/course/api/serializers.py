from rest_framework import serializers
from course.models import Course

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('course_content',)

class OutCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('school', 'course_content', 'id')

        