from channels.generic.websocket import AsyncWebsocketConsumer
from django.template import Context, Template
import json
import logging 
from .models import Notification

logger = logging.getLogger(__file__)

class NotificationConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.user = self.scope["user"]
        await self.channel_layer.group_add(f"notification_{self.user.id}", self.channel_name)
        await self.accept()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(f"notification_{self.user.id}", self.channel_name)
        
    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
        except json.JSONDecodeError as e:
            logger.exception(e)
            return
        read = text_data_json.get("read", None)
        notif_id = text_data_json.get("notification_id", None)
        try:
            notif = await Notification.objects.aget(id=notif_id)
            notif.read = read
            await notif.asave()
        except Notification.DoesNotExist as e:
            logger.exception(e)
        except Exception as e:
            logger.exception(e)

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