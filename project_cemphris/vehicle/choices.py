from django.db import models

class VehicleChoices(models.IntegerChoices):
    MOTORBIKE= 1 
    CAR = 2
    TRUCK = 3

class VehicleTypeChoices(models.IntegerChoices):
    MANUAL = 1
    AUTOMATIC = 2