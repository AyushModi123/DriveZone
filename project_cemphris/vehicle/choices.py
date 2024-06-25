from django.db import models

class VehicleChoices(models.TextChoices):
    MOTORBIKE= 'motorbike', 'Motorbike'
    CAR = 'car', 'Car'
    TRUCK = 'truck', 'Truck'

class VehicleTypeChoices(models.TextChoices):
    MANUAL = 'manual', 'Manual'
    AUTOMATIC = 'automatic', 'Automatic'