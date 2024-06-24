from django.db import models

# Create your models here.
class Booking(models.Model):
    instructor = models.ForeignKey('base.Instructor', on_delete=models.CASCADE, related_name='booking')
    learner = models.ForeignKey('base.Learner', on_delete=models.CASCADE, related_name='booking')
    payment = models.ForeignKey('payment.Payment', on_delete=models.CASCADE, related_name='booking', default=1)
    slot = models.ForeignKey('slot.Slot', on_delete=models.CASCADE, related_name='booking', default=1)
    booked_on = models.DateTimeField(auto_created=True, auto_now=True)

    class Meta:
        db_table = "bookings"