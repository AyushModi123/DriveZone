from django.utils import timezone
from django.core.exceptions import ValidationError


def validate_start_time(value):
    if value < timezone.now():
        raise ValidationError("Start time cannot be in the past.")