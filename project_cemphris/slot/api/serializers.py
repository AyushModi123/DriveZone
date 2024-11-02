from rest_framework import serializers
from datetime import datetime
from slot.models import Slot

class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slot
        fields = ('start_time', 'duration', 'instructor')

class OutSlotSerializer(serializers.ModelSerializer):
    inst_name = serializers.SerializerMethodField()
    inst_id = serializers.SerializerMethodField()

    class Meta:
        model = Slot
        fields = ('id', 'inst_id', 'inst_name', 'start_time', 'duration', 'is_booked', 'learner')

    def get_inst_name(self, obj):
        return obj.instructor.full_name

    def get_inst_id(self, obj):
        return obj.instructor.id

class OutShortSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slot
        fields = ('id', 'instructor', 'start_time', 'duration', 'is_booked')