from django.conf import settings
from django.contrib.auth import get_user_model
from jwt import decode as jwt_decode
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import DenyConnection
from channels.db import database_sync_to_async
import json
import logging 
from .models import Notification

logger = logging.getLogger(__file__)

User = get_user_model()

class NotificationConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.user = None
        await self.accept()
    
    async def disconnect(self, close_code):
        if self.user:
            await self.channel_layer.group_discard(f"notification_{self.user.id}", self.channel_name)        
            await self.close(200, "Closed on request")
        
    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
        except json.JSONDecodeError as e:
            logger.exception(e)
            return
        if text_data_json.get("type", None) == "authenticate":
            token = text_data_json.get("token", None)
            if token:
                self.user = await self.get_user_from_jwt(token)
            else:
                await self.send(
                text_data=json.dumps(
                        {
                            'type': 'authentication_failed'
                        }
                    )
                )
        elif self.user:
            if text_data_json.get("type", None) == "message":
                data = text_data_json.get("data", None)
                if data:
                    read = data.get("read", None)
                    notif_id = data.get("notification_id", None)
                    try:
                        notif = await Notification.objects.aget(id=notif_id)
                        notif.read = read
                        await notif.asave()
                    except Notification.DoesNotExist as e:
                        logger.exception(e)
                    except Exception as e:
                        logger.exception(e)
        else:
            await self.send(
                text_data=json.dumps(
                    {
                        'type': 'authentication_failed'
                    }
                )
            )

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

    @database_sync_to_async
    def get_user_from_jwt(self, token):
        try:
            decoded_token = jwt_decode(token, settings.SECRET_KEY, algorithms=settings.SIMPLE_JWT.get('ALGORITHM', 'HS256'))
            user = User.objects.get(id=decoded_token['user_id'])
            return user
        except Exception:
            return None