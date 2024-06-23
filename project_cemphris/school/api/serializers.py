from rest_framework import serializers
from school.models import School

class SchoolSerializer(serializers.Serializer):
    class Meta:
        model = School
        fields = ('name','description', 'email', 'location', 'mobile_number', 'preferred_language')