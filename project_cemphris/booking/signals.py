from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Booking

@receiver(post_save, sender=Booking)
def set_slot_booked(sender, instance, created, **kwargs):
    if created:
        slot = instance.slot
        slot.is_booked = True
        slot.save()