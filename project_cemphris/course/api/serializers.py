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
    
class OutShortEnrollCourseSerializer(serializers.ModelSerializer):
    inst_name = serializers.SerializerMethodField()
    inst_id = serializers.SerializerMethodField()
    course = OutCourseSerializer()
    
    class Meta:
        model = EnrollCourse
        fields = ('course', 'inst_name', 'inst_id')

    def get_inst_name(self, obj):
        return obj.instructor.full_name
    
    def get_inst_id(self, obj):
        return obj.instructor.id

class OutEnrollCourseSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = EnrollCourse
        fields = ('id', 'learner', 'course', 'instructor', 'payment')