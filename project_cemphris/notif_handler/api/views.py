from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from django.conf import settings
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers
from notif_handler.models import Notification
from notif_handler.constants import DEFAULT_RETURN_NOTIFICATION_COUNT
from .serializers import OutNotificationSerializer

@cache_page(settings.CACHE_TTL)
@vary_on_headers("Authorization")
@api_view(["GET"])
def get_notifications(request):
    current_user = request.user    
    notifications = Notification.objects.filter(user=current_user).order_by('-created_at')[:DEFAULT_RETURN_NOTIFICATION_COUNT]
    return Response({"notifications": OutNotificationSerializer(notifications, many=True).data}, status=200)
        