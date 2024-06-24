from rest_framework import serializers
from django.contrib.auth import get_user_model
from base.choices import RoleChoices
from base.models import Instructor, LicenseInformation, Learner, School

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']

class OutUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'role', 'profile_completion_level')

class LearnerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Learner
        fields = ['user', 'full_name', 'location', 'image_url', 'mobile_number', 'preferred_language']

    def create(self, validated_data):
        is_active = validated_data.pop('is_active')
        user_data = validated_data.pop('user')
        user = User.objects.create(role=RoleChoices.LEARNER, is_active=is_active, **user_data)
        learner = Learner.objects.create(user=user, **validated_data)
        return learner

class OutLearnerSerializer(serializers.ModelSerializer):
    user = OutUserSerializer()

    class Meta:
        model = Learner
        fields = ('user', 'full_name', 'location', 'image_url', 'mobile_number', 'preferred_language')

class SchoolSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = School
        fields = ['user', 'name', 'location', 'image_url', 'mobile_number', 'preferred_language']
    
    def create(self, validated_data):
        is_active = validated_data.pop('is_active')
        user_data = validated_data.pop('user')
        user = User.objects.create(role=RoleChoices.SCHOOL, is_active=is_active, **user_data)
        school = School.objects.create(user=user, **validated_data)
        return school

class OutSchoolSerializer(serializers.ModelSerializer):
    user = OutUserSerializer()

    class Meta:
        model = School
        fields = ['user', 'name', 'location', 'image_url', 'mobile_number', 'preferred_language']

class OutInstructorSerializer(serializers.ModelSerializer):
    user = OutUserSerializer()
    school = OutSchoolSerializer()
    area_of_expertise = serializers.SerializerMethodField()

    class Meta:
        model = Instructor
        fields = ['user', 'school', 'full_name', 'location', 'image_url', 'mobile_number', 'preferred_language', 'experience', 'area_of_expertise']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Removing user data of School as it is not needed here        
        if 'school' in representation:
            if 'user' in representation['school']:
                representation['school'].pop('user', None)
        
        return representation

    def get_area_of_expertise(self, obj):
        return obj.get_area_of_expertise_display()

class LicenseInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LicenseInformation
        fields = ('number', 'type', 'expiration_date', 'issuing_authority')
