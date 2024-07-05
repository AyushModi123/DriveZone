from django.utils import timezone
from celery import shared_task
from .models import ScheduledEmail
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from notif_handler.utils import send_scheduled_email

@shared_task(name='notif_handler.tasks.send_scheduled_emails')
def send_scheduled_emails():
    due_emails = ScheduledEmail.objects.filter(
                scheduled_time__lte=timezone.now(),
                status='PENDING'
            )
    for email in due_emails:
        send_scheduled_email(email)
        print(f"Sent email {email.id}")

@shared_task(name='notif_handler.tasks.send_notification')
def send_notification(group_name, event):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        group_name,
        event   
    )