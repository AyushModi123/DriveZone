from django.db import models

class PaymentStatusTypeChoices(models.TextChoices):
    PENDING = ('pending', "Pending")
    FAILED = ('failed', "Failed")
    COMPLETE = ('complete', "Complete")