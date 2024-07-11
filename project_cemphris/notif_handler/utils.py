from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from notif_handler.models import ScheduledEmail
from notif_handler.tasks import send_email
# class EmailRateLimiter:
#     def __init__(self, key_prefix='email_rate_limit', limit=100, period=3600):
#         self.key_prefix = key_prefix
#         self.limit = limit
#         self.period = period

#     def is_allowed(self, user_id):
#         key = f"{self.key_prefix}:{user_id}"
#         count = cache.get(key, 0)
#         if count >= self.limit:
#             return False
#         cache.set(key, count + 1, self.period)
#         return True

# rate_limiter = EmailRateLimiter()

# def send_email(subject, recipient, message):
#     """Sends email synchronously right away"""
#     try:
#         send_mail(
#             subject=subject,
#             message=message,
#             from_email=None,  # Uses DEFAULT_FROM_EMAIL from settings
#             recipient_list=[recipient],
#             fail_silently=False,
#         )
#         return True
#     except Exception as e:
#         print(f"Error sending email synchronously: {str(e)}")
#         return False


def schedule_email(subject, recipient, body, scheduled_time):
    """
    Schedules email to send at a scheduled_time
    Send scheduled_time in +5:30 GMT
    """

    # if not rate_limiter.is_allowed(user.id):
    #     raise PermissionDenied("Email rate limit exceeded")
    email = ScheduledEmail.objects.create(
        subject=subject,
        body=body,
        recipient=recipient,        
        scheduled_time=scheduled_time,
    )
    email.save()
    return

def send_scheduled_email(scheduled_email):
    subject = scheduled_email.subject
    body = scheduled_email.body
    recipient = scheduled_email.recipient
    send_email.delay(subject=subject, body=body, recipient=recipient)
    
