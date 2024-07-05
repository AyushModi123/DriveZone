from rest_framework import serializers
from payment.models import PaymentDetail

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentDetail
        fields = ('course', )
