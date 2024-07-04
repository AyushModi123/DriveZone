from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from notif_handler.tasks import send_scheduled_emails

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_cemphris.settings')

app = Celery('project_cemphris')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
