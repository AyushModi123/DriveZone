from django.apps import apps
from django.core.exceptions import ImproperlyConfigured
from django.template.loader import render_to_string
from django.utils import timezone
from django.db.models.signals import post_save, pre_save

from django.dispatch import receiver

from project_cemphris.services import schedule_email
from notif_handler.models import ScheduledEmail
from .constants import LEARNER_REMINDER_SUBJECT, INSTRUCTOR_REMINDER_SUBJECT
try:
    Slot = apps.get_model('slot', 'Slot')
    if Slot is None:
        raise ImproperlyConfigured("Model 'Slot' not found in app 'slot'")
except LookupError as e:
    raise ImproperlyConfigured(f"Error loading model: {e}")

@receiver(post_save, sender=Slot)
def schedule_learner_slot_reminder(sender, instance, created, **kwargs):
    if instance.check_learner:
        if created:
            # Learner
            body = render_to_string('notif_handler/learner_reminder.html', {
                        'name': instance.learner.full_name,
                        'class_time': instance.start_time.astimezone().strftime('%Y-%m-%d %H:%M')
            })
            scheduled_time = instance.start_time - timezone.timedelta(minutes=30)
            schedule_email(subject=LEARNER_REMINDER_SUBJECT, recipient=instance.learner.user.email, body=body, scheduled_time=scheduled_time)
            # Instructor
            body = render_to_string('notif_handler/instructor_reminder.html', {
                        'name': instance.instructor.full_name,
                        'class_time': instance.start_time.astimezone().strftime('%Y-%m-%d %H:%M')
            })
            scheduled_time = instance.start_time - timezone.timedelta(minutes=30)
            schedule_email(subject=INSTRUCTOR_REMINDER_SUBJECT, recipient=instance.instructor.user.email, body=body, scheduled_time=scheduled_time)
        else:
            # Handle logic for updation in slot details
            pass