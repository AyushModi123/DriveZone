from rest_framework import serializers
from notif_handler.models import Notification

class OutNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('id', 'message', 'read', 'created_at', 'tag')