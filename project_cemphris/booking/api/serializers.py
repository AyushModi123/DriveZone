from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.utils.timesince import timesince
from booking.models import Booking

class BookingSerializer(ModelSerializer):
    class Meta:
        model = Booking
        exclude = ('booked_on')