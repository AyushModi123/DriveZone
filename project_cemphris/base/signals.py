from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import LicenseInformation, Instructor, Learner
from .choices import ProfileCompletionLevelChoices

@receiver(post_save, sender=LicenseInformation)
def update_license_profile_completion_level(sender, instance, created, **kwargs):
    if created:
        profile_completion_level = instance.user.profile_completion_level
        if profile_completion_level < ProfileCompletionLevelChoices.COMPLETE.value:
            instance.user.profile_completion_level+=1
            instance.save()

@receiver(pre_save, sender=Instructor)
def update_instructor_details_profile_completion_level(sender, instance, **kwargs):    
    try:
        existing_instance = Instructor.objects.get(pk=instance.pk)
        if existing_instance.experience is None and instance.experience is not None:
            profile_completion_level = instance.user.profile_completion_level
            if profile_completion_level < ProfileCompletionLevelChoices.COMPLETE.value:
                instance.user.profile_completion_level+=1
                instance.save()
    except Instructor.DoesNotExist:
        pass

# @receiver(pre_save, sender=Learner)
# def update_learner_details_profile_completion_level(sender, instance, **kwargs):    
    # try:
        # existing_instance = Learner.objects.get(pk=instance.pk)
        # if existing_instance.experience is None and instance.experience is not None:
            # profile_completion_level = instance.user.profile_completion_level
    #         if profile_completion_level < ProfileCompletionLevelChoices.COMPLETE.value:
    #             instance.user.profile_completion_level+=1
    # except Learner.DoesNotExist:
    #     pass