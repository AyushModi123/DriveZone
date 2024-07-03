from django.utils import timezone
from celery import shared_task
from .models import ScheduledEmail
from .utils import send_scheduled_email

@shared_task
def send_scheduled_emails():
    due_emails = ScheduledEmail.objects.filter(
                scheduled_time__lte=timezone.now(),
                status='PENDING'
            )
    for email in due_emails:
        send_scheduled_email(email)
        print(f"Sent email {email.id}")