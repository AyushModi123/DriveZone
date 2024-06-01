from django.db import models

class VehicleChoices(models.IntegerChoices):
    MOTORBIKE= 1 
    CAR = 2
    TRUCK = 3

class Vehicle(models.Model):

    instructor = models.ForeignKey('base.Instructor', on_delete=models.CASCADE, related_name='vehicle')
    image_url = models.URLField(null=False, blank=True, default='')
    model = models.CharField(max_length=50, null=False, blank=False, default='XXXXX')
    make = models.IntegerField(choices=VehicleChoices.choices, null=False, blank=False)
    license_no = models.CharField(max_length=10, null=False, blank=False, default='XX000000')

    def __str__(self):
        return f"id: {self.id}->{self.get_make_display()} with model {self.model}"
    