from rest_framework import serializers
from slot.models import Slot

class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slot
        fields = ('slot_start', 'duration')

class SemiSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slot
        exclude = ('instructor',)