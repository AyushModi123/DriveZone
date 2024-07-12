from django.db import models
from .choices import PaymentStatusTypeChoices

# Create your models here.
class PaymentDetail(models.Model):

    school = models.ForeignKey("base.School", on_delete=models.CASCADE, related_name="transactions")
    learner = models.ForeignKey("base.Learner", on_delete=models.CASCADE, related_name="payments")
    status = models.CharField(choices=PaymentStatusTypeChoices.choices, null=False, blank=False, default=PaymentStatusTypeChoices.PENDING)