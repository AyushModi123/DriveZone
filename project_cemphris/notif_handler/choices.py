from django.db import models

class StatusChoices(models.TextChoices):
    PENDING = ('PENDING', 'Pending')
    SENT = ('SENT', 'Sent')
    FAILED = ('FAILED', 'Failed')