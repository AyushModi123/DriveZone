from django.db import models

class VehicleChoices(models.IntegerChoices):
    MOTORBIKE= 1 
    CAR = 2
    TRUCK = 3

class Vehicle(models.Model):

    instructor = models.OneToOneField('base.Instructor', on_delete=models.CASCADE, related_name='vehicle')
    # image = models.ImageField(null=True, default="avatar.svg")
    model = models.CharField(max_length=50, null=True, blank=True)
    make = models.IntegerField(choices=VehicleChoices.choices)

    def __str__(self):
        return f"{self.make} with model {self.model}"
    