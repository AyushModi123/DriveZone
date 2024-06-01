from rest_framework import serializers
from vehicle.models import Vehicle

class InstructorVehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        exclude = ('instructor',)

class LearnerVehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        exclude = ('license_no',)