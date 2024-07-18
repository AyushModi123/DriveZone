from rest_framework import serializers
from datetime import datetime
from slot.models import Slot

class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slot
        fields = ('start_time', 'duration', 'instructor')

class OutSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slot
        fields = ('instructor', 'start_time', 'duration', 'is_booked', 'learner')

class OutShortSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slot
        fields = ('instructor', 'start_time', 'duration', 'is_booked')