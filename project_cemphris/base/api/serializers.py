from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from project_cemphris.serializers import OutCourseSerializer
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
        # add instructor validation to not create instructor
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

class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email',)

class ResetPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = User
        fields = ('password', 'password2')

class LearnerSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Learner
        fields = ['full_name', 'location', 'mobile_number', 'preferred_language']

    def create(self, validated_data):
        user = validated_data.pop('user')
        learner = Learner.objects.create(user=user, **validated_data)
        return learner

class OutLicenseInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LicenseInformation
        fields = ('number', 'type', 'expiration_date', 'issuing_authority', 'image_url')

class OutLearnerSerializer(serializers.ModelSerializer):
    user = OutUserSerializer()
    license = OutLicenseInformationSerializer(allow_null=True)
    course = OutCourseSerializer(allow_null=True)
    class Meta:
        model = Learner
        fields = ('id', 'user', 'course', 'full_name', 'license', 'location', 'image_url', 'mobile_number', 'preferred_language')

class SchoolSerializer(serializers.ModelSerializer):    

    class Meta:
        model = School
        fields = ['name', 'location', 'mobile_number', 'preferred_language', 'desc']
    
    def create(self, validated_data):        
        user = validated_data.pop('user')
        school = School.objects.create(user=user, **validated_data)
        return school

class OutSchoolSerializer(serializers.ModelSerializer):
    user = OutUserSerializer()

    class Meta:
        model = School
        fields = ['id', 'user', 'name', 'location', 'image_url', 'mobile_number', 'preferred_language', 'desc']

class OutVeryShortSchoolSerializer(serializers.ModelSerializer):

    class Meta:
        model = School
        fields = ['id', 'name', 'location', 'image_url', 'preferred_language']

class OutShortSchoolSerializer(serializers.ModelSerializer):

    class Meta:
        model = School
        fields = ['id', 'name', 'location', 'image_url', 'mobile_number', 'preferred_language', 'desc']


class OutInstructorSerializer(serializers.ModelSerializer):
    user = OutUserSerializer()
    school = OutSchoolSerializer()
    license = OutLicenseInformationSerializer(allow_null=True)
    area_of_expertise = serializers.SerializerMethodField()

    class Meta:
        model = Instructor
        fields = ['id', 'user', 'school', 'license', 'full_name', 'location', 'image_url', 'mobile_number', 'preferred_language', 'experience', 'area_of_expertise']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Removing user data of School as it is not needed here        
        if 'school' in representation:
            if 'user' in representation['school']:
                representation['school'].pop('user', None)
        
        return representation

    def get_area_of_expertise(self, obj):
        """Called for area_of_expertise serializer field"""
        return obj.get_area_of_expertise_display()

class LicenseInformationSerializer(serializers.ModelSerializer):    
    class Meta:
        model = LicenseInformation
        fields = ('number', 'type', 'expiration_date', 'issuing_authority')
    
    def create(self, validated_data):
        image_url = validated_data.pop('image_url')
        user = validated_data.pop('user')
        license = LicenseInformation.objects.create(user=user, image_url=image_url, **validated_data)
        return license

    def update(self, validated_data):
        image_url = validated_data.pop('image_url')
        license = LicenseInformation.objects.update(image_url=image_url, **validated_data)
        return license

class OutShortInstructorSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Instructor
        fields = ('id', 'email', 'full_name', 'location', 'image_url', 'preferred_language', 'experience')

class InstructorSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    class Meta:
        model = Instructor
        fields = ('email', 'full_name', 'location', 'mobile_number', 'preferred_language', 'experience', 'area_of_expertise')

    def create(self, validated_data):
        is_active = validated_data.pop('is_active', False)
        password = validated_data.pop('password', None)
        school = validated_data.pop('school', None)
        email = validated_data.pop('email', None)
        user = User.objects.create(            
            email=email,
            role=RoleChoices.INSTRUCTOR,
            is_active=is_active,
        )
        user.set_password(password)
        user.save()
        instructor = Instructor.objects.create(
            user=user,
            school=school,
            **validated_data
        )
        instructor.save()
        return instructor