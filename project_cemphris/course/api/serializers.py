import logging
from rest_framework import serializers
from course.models import Course, EnrollCourse
from review.models import Review

logger = logging.getLogger(__file__)

class CourseSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(required=False, default=True)
    class Meta:
        model = Course
        fields = ('course_content', 'title', 'price', 'is_active')

class OutShortSchoolCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('school', 'id', 'title', 'price', 'is_active')

class OutSchoolCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('school', 'course_content', 'id', 'title', 'price', 'is_active')

class OutShortCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('school', 'id', 'title', 'price')

class OutCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('school', 'course_content', 'id', 'title', 'price')

class EnrollCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnrollCourse
        fields = ('learner', 'course', 'instructor')    
    
class OutLearnerEnrollCourseSerializer(serializers.ModelSerializer):
    inst_name = serializers.SerializerMethodField()
    inst_id = serializers.SerializerMethodField()
    course = OutCourseSerializer()
    review_id = serializers.SerializerMethodField()
    
    class Meta:
        model = EnrollCourse
        fields = ('course', 'inst_name', 'inst_id', 'review_id', 'created_at', 'payment')

    def get_inst_name(self, obj):
        return obj.instructor.full_name
    
    def get_inst_id(self, obj):
        return obj.instructor.id
    
    def get_review_id(self, obj):
        review_id = None
        try:
            review = Review.objects.get(learner=obj.learner)
            review_id = review.pk
        except Review.DoesNotExist:
            logger.info("Review does not exist")
        return review_id

class OutEnrollCourseSerializer(serializers.ModelSerializer):    
    inst_name = serializers.SerializerMethodField()
    learner_name = serializers.SerializerMethodField()
    course_id = serializers.SerializerMethodField()
    course_name = serializers.SerializerMethodField()

    class Meta:
        model = EnrollCourse
        fields = ('id', 'inst_name', 'learner_name', 'learner', 'course_id', 'course_name', 'instructor', 'payment', 'created_at')
    
    def get_inst_name(self, obj):
        return obj.instructor.full_name

    def get_learner_name(self, obj):
        return obj.learner.full_name
    
    def get_course_id(self, obj):
        return obj.course.pk
    
    def get_course_name(self, obj):
        return obj.course.title
