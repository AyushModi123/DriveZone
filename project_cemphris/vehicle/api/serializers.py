from rest_framework import serializers
from vehicle.models import Vehicle

class InstructorVehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'

class LearnerVehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        exclude = ('license_no')