from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from notif_handler.models import Notification
from notif_handler.constants import RETURN_NOTIFICATION_COUNT
from .serializers import OutNotificationSerializer

@api_view(["GET"])
def get_notifications(request):
    current_user = request.user    
    notifications = Notification.objects.filter(user=current_user).order_by('-created_at')[:RETURN_NOTIFICATION_COUNT]
    return Response({"notifications": OutNotificationSerializer(notifications).data}, status=200)
        