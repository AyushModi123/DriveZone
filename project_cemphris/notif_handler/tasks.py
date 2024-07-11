import logging
from django.utils import timezone
from django.core.mail import send_mail
from celery import shared_task
from .models import ScheduledEmail
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from notif_handler.constants import MAX_EMAIL_RETRY_COUNT

logger = logging.getLogger(__name__)

@shared_task(name='notif_handler.tasks.send_scheduled_emails')
def send_scheduled_emails():
    due_emails = ScheduledEmail.objects.filter(
                scheduled_time__lte=timezone.now(),
                status='PENDING'
            )
    for email in due_emails:
        try:
            send_mail(
                subject=email.subject,
                message=email.body,
                from_email=None,  # Uses DEFAULT_FROM_EMAIL from settings
                recipient_list=[email.recipient],
                fail_silently=False,
            )
            email.status = 'SENT'
            print(f"Sent email {email.id}")
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            email.retry_count += 1
            if email.retry_count >= MAX_EMAIL_RETRY_COUNT:
                email.status = 'FAILED'
        email.save()

@shared_task(name='notif_handler.tasks.send_notification')
def send_notification(group_name, event):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        group_name,
        event   
    )

@shared_task(name='notif_handler.tasks.send_email')
def send_email(subject, recipient, message):
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=None,  # Uses DEFAULT_FROM_EMAIL from settings
            recipient_list=[recipient],
            fail_silently=False,
        )
        logger.info(f"Email sent to {recipient}")
    except Exception as e:
        logger.exception(e)
    