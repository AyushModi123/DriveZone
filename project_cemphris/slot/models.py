from django.db import models
from django.utils import timezone
# Create your models here.

class Slot(models.Model):
    instructor = models.ForeignKey("base.Instructor", on_delete=models.CASCADE, related_name="slot")
    slot_start = models.DateTimeField(null=False, blank=False, default=timezone.now)    
    duration = models.DurationField(null=False, blank=False)
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"Slot{" booked for" if self.is_booked else " available on"} {self.slot_start} for {self.duration} hours"
