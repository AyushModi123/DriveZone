from django.db import models
from django.contrib.auth import get_user_model
from .choices import StatusChoices

User = get_user_model()

class ScheduledEmail(models.Model):

    slot = models.ForeignKey('slot.Slot', on_delete=models.CASCADE, related_name='reminder')
    subject = models.CharField(max_length=255, blank=True, null=False)
    body = models.TextField(blank=True, null=False)
    recipient = models.EmailField(null=False, blank=False)
    scheduled_time = models.DateTimeField(null=False, blank=False)
    status = models.CharField(max_length=10, choices=StatusChoices.choices, default=StatusChoices.PENDING, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    retry_count = models.SmallIntegerField(default=0, null=False, blank=False)

class Notification(models.Model):
    user = models.ForeignKey('base.User', on_delete=models.CASCADE, related_name='notifications', null=False, blank=False)
    message = models.TextField()
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    tag = models.CharField(max_length=255, blank=True, default='default')

    def __str__(self):
        return self.message        