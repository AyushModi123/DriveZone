from django.db import models

class DurationChoices(models.IntegerChoices):
    THIRTY_MINUTES = 30, '30 minutes'
    ONE_HOUR = 60, '1 hour'
    NINETY_MINUTES = 90, '1.5 hours'
    TWO_HOURS = 120, '2 hours'