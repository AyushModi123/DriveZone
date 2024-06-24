from rest_framework import serializers
from django.contrib.auth import get_user_model
from base.choices import RoleChoices
from base.models import Instructor, LicenseInformation, Learner, School

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']

class LearnerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Learner
        fields = ['full_name', 'location', 'image_url', 'mobile_number', 'preferred_language']

    def create(self, validated_data):
        is_active = validated_data.pop('is_active')
        user_data = validated_data.pop('user')
        user = User.objects.create(role=RoleChoices.LEARNER, is_active=is_active, **user_data)
        learner = Learner.objects.create(user=user, **validated_data)
        return learner

class SchoolSerializer(serializers.Serializer):
    user = UserSerializer()

    class Meta:
        model = School
        fields = ['name', 'location', 'image_url', 'mobile_number', 'preferred_language']
    
    def create(self, validated_data):
        is_active = validated_data.pop('is_active')
        user_data = validated_data.pop('user')
        user = User.objects.create(role=RoleChoices.SCHOOL, is_active=is_active, **user_data)
        school = School.objects.create(user=user, **validated_data)
        return school

class InstructorDetailsSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Instructor
        fields = ['full_name', 'location', 'image_url', 'mobile_number', 'preferred_language', 'experience', 'area_of_expertise']

class LearnerDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Learner
        exclude = ('user', )

class LicenseInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LicenseInformation
        fields = ('number', 'type', 'expiration_date', 'issuing_authority')
