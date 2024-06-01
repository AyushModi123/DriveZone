from django.contrib import admin

# Register your models here.
from .models import PaymentHistory

admin.site.register(PaymentHistory)