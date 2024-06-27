from django.db import models
from django.core.exceptions import ValidationError
from datetime import timedelta
from .choices import DurationChoices
from .validators import validate_start_time
# Create your models here.



class Slot(models.Model):    

    school = models.ForeignKey("base.School", on_delete=models.CASCADE, related_name="slots")
    instructor = models.ForeignKey("base.Instructor", on_delete=models.CASCADE, related_name="teaching_slots")
    start_time = models.DateTimeField(null=False, blank=False, validators=[validate_start_time])
    duration = models.IntegerField(choices=DurationChoices.choices, default=DurationChoices.ONE_HOUR)
    is_booked = models.BooleanField(default=False)

    @property
    def end_time(self):
        return self.start_time + timedelta(minutes=self.duration)

    def clean(self):
        """ Overrides default clean method
        Checks overlapping of instructor slots """
        if self.pk is None:  # Only check when creating a new instance
            end_time = self.start_time + timedelta(minutes=self.duration)
            overlapping_slots = Slot.objects.filter(
                instructor=self.instructor,
                start_time__lt=end_time,
                start_time__gte=self.start_time
            )
            if overlapping_slots.exists():
                raise ValidationError("This slot overlaps with an existing slot for this instructor.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Slot {'booked for' if self.is_booked else 'available on'} {self.start_time.astimezone().strftime('%Y-%m-%d %H:%M')} for {self.duration} minutes"

    class Meta:
        ordering = ['school', 'start_time', 'instructor']
        constraints = [
            models.UniqueConstraint(fields=['school', 'instructor', 'start_time'], name='unique_instructor_slot')
        ]