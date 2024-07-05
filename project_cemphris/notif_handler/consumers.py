from channels.generic.websocket import AsyncWebsocketConsumer
from django.template import Context, Template
import json 
from .models import Notification

class NotificationConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.user = self.scope["user"]
        await self.channel_layer.group_add(f"notification_{self.user.id}", self.channel_name)
        await self.accept()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(f"notification_{self.user.id}", self.channel_name)
        
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        read = text_data_json["read"]
        notif_id = text_data_json["notification_id"]
        try:
            notif = Notification.objects.get(id=notif_id)
            notif.read = read
            notif.save()
        except Notification.DoesNotExist:
            pass

    async def send_notification(self, event):
        message = event["message"]
        tag = event["tag"]
        course_id = event["course_id"]
        learner_id = event["learner_id"]
        notif_id = event["notification_id"]
        await self.send(
            text_data=json.dumps(
            {               
                'tag': tag,
                'course_id': course_id,
                'learner_id': learner_id,
                'notification_id': notif_id,
                "message": message
            }
            )
        )