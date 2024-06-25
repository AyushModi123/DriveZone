from rest_framework import serializers
from vehicle.models import Vehicle

class VehicleSerializer(serializers.ModelSerializer):
    make = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    class Meta:
        model = Vehicle
        fields = ('model', 'make', 'type', 'license_no')

    def create(self, validated_data):
        image_url = validated_data.pop('image_url')
        school = validated_data.pop('school')
        vehicle = Vehicle.objects.create(school=school, image_url=image_url, **validated_data)
        return vehicle

    def update(self, validated_data):
        image_url = validated_data.pop('image_url')        
        vehicle = Vehicle.objects.update(image_url=image_url, **validated_data)
        return vehicle

    def get_make(self, obj):
        """Called for make serializer field"""
        return obj.get_make_display()
    
    def get_type(self, obj):
        """Called for type serializer field"""
        return obj.get_type_display()

class OutShortVehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ('id', 'model', 'make', 'type', 'license_no', 'image_url')

class VehicleIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ('id', )

# class LearnerVehicleSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Vehicle
#         exclude = ('license_no',)