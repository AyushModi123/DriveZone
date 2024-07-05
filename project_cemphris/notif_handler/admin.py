from django.contrib import admin
from .models import ScheduledEmail, Notification

admin.site.register(ScheduledEmail)
admin.site.register(Notification)
