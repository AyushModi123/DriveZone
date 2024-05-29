from django.db import models

class PaymentMethod(models.IntegerChoices):
    CREDIT_CARD = 1
    DEBIT_CARD = 2
    CASH = 3

class Payment(models.Model):
    learner = models.ForeignKey('base.Learner', on_delete=models.CASCADE, related_name='payment')
    payment_method = models.IntegerField(choices=PaymentMethod)
    created_on = models.DateTimeField(auto_created=True, auto_now=True)