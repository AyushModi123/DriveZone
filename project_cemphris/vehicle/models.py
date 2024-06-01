from django.db import models

class VehicleChoices(models.IntegerChoices):
    MOTORBIKE= 1 
    CAR = 2
    TRUCK = 3

class Vehicle(models.Model):

    instructor = models.ForeignKey('base.Instructor', on_delete=models.CASCADE, related_name='vehicle')
    # image = models.ImageField(null=True, default="avatar.svg")
    model = models.CharField(max_length=50, null=True, blank=True)
    make = models.IntegerField(choices=VehicleChoices.choices)
    license_no = models.CharField(max_length=10, null=False, blank=False, default='XX000000')

    def __str__(self):
        return f"{self.get_make_display()} with model {self.model}"
    