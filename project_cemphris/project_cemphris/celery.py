from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
import django
from django.conf import settings

django.setup()

from notif_handler.tasks import send_scheduled_emails

app = Celery('project_cemphris', broker=settings.CELERY_BROKER_URL)

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.control.rate_limit('notif_handler.tasks.send_email', '1/m')
app.control.rate_limit('notif_handler.tasks.send_scheduled_emails', '1/m')