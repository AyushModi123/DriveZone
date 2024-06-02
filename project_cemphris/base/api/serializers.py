from rest_framework import serializers
from django.contrib.auth import get_user_model
from base.models import Instructor, LicenseInformation, Learner

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'dob', 'preferred_language', 'mobile_number')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

class InstructorDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instructor
        fields = ('experience', 'area_of_expertise')

class LearnerDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Learner
        exclude = ('user', )

class LicenseInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LicenseInformation
        fields = ('number', 'type', 'expiration_date', 'issuing_authority')
