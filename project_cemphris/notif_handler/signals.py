from django.apps import apps
from django.core.exceptions import ImproperlyConfigured
from django.template.loader import render_to_string
from django.utils import timezone
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from project_cemphris.services import schedule_email
from notif_handler.models import ScheduledEmail, Notification
from .constants import LEARNER_REMINDER_SUBJECT, INSTRUCTOR_REMINDER_SUBJECT, NotificationTag
from notif_handler.tasks import send_notification

try:
    Slot = apps.get_model('slot', 'Slot')
    if Slot is None:
        raise ImproperlyConfigured("Model 'Slot' not found in app 'slot'")
except LookupError as e:
    raise ImproperlyConfigured(f"Error loading model: {e}")

try:
    EnrollCourse = apps.get_model('course', 'EnrollCourse')
    if EnrollCourse is None:
        raise ImproperlyConfigured("Model 'EnrollCourse' not found in app 'course'")
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

@receiver(post_save, sender=EnrollCourse)
def send_notification(sender, instance, created, **kwargs):
    if created:
        learner = instance.learner
        course = instance.course
        school = course.school
        message = f'{learner.full_name} just enrolled.\n Assign Instructor here'
        notif = Notification.objects.create(
            user=school.user,
            message=message,
            tag=NotificationTag.NEW_ENROLL
        )
        notif.save()
        group_name = f'notification_{school.user.id}'
        event = {
            'type': 'send_notification',
            'tag': NotificationTag.NEW_ENROLL,
            'notification_id': notif.id,
            'course_id': course.id,
            'learner_id': learner.id,
            'message': message
        }
        send_notification.delay(group_name, event)

@receiver(post_save, sender=EnrollCourse)
def instructor_assigned(sender, instance, created, **kwargs):    
    if instance.is_instructor_assigned:
        learner = instance.learner
        course = instance.course
        instructor = instance.instructor        
        message = f'You have been assigned {instructor.full_name} as your instructor.'
        notif = Notification.objects.create(
            user=learner.user,
            message=message,
            tag=NotificationTag.INSTRUCTOR_ASSIGNED
        )
        notif.save()
        group_name = f'notification_{learner.user.id}'
        event = {
            'type': 'send_notification',
            'tag': NotificationTag.INSTRUCTOR_ASSIGNED,
            'notification_id': notif.id,                                
            'message': message
        }
        send_notification.delay(group_name, event)

@receiver(post_save, sender=EnrollCourse)
def instructor_assigned(sender, instance, created, **kwargs):    
    if instance.is_instructor_assigned:
        learner = instance.learner        
        instructor = instance.instructor        
        message = f'New learner assigned {learner.full_name}'
        notif = Notification.objects.create(
            user=instructor.user,
            message=message,
            tag=NotificationTag.LEARNER_ASSIGNED
        )
        notif.save()
        group_name = f'notification_{instructor.user.id}'
        event = {
            'type': 'send_notification',
            'tag': NotificationTag.LEARNER_ASSIGNED,
            'notification_id': notif.id,
            'learner_id': learner.id,                                
            'message': message
        }
        send_notification.delay(group_name, event)