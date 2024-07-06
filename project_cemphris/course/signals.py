from django.db.models.signals import post_save
from django.dispatch import receiver
from payment.models import PaymentDetail
from payment.choices import PaymentStatusTypeChoices
from .models import EnrollCourse

@receiver(post_save, sender=PaymentDetail)
def enroll_course(sender, instance, created, **kwargs):
    if created:
        if instance.status == PaymentStatusTypeChoices.COMPLETE:
            learner_course = EnrollCourse.objects.create(
                learner=instance.learner,
                course=instance.course
            )
            learner_course.save()
