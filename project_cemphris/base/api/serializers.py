from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from base.choices import RoleChoices
from base.models import Instructor, LicenseInformation, Learner, School

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'password2', 'role']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        
        return attrs

    def create(self, validated_data):
        is_active = validated_data.pop('is_active', False)        
        user = User.objects.create(            
            email=validated_data['email'],
            role=validated_data['role'],
            is_active=is_active,            
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class OutUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'role', 'profile_completion_level', 'is_active')

class LearnerSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Learner
        fields = ['full_name', 'location', 'mobile_number', 'preferred_language']

    def create(self, validated_data):
        user = validated_data.pop('user')
        learner = Learner.objects.create(user=user, **validated_data)
        return learner

class OutLearnerSerializer(serializers.ModelSerializer):
    user = OutUserSerializer()

    class Meta:
        model = Learner
        fields = ('user', 'full_name', 'location', 'image_url', 'mobile_number', 'preferred_language')

class SchoolSerializer(serializers.ModelSerializer):    

    class Meta:
        model = School
        fields = ['name', 'location', 'mobile_number', 'preferred_language']
    
    def create(self, validated_data):        
        user = validated_data.pop('user')
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
