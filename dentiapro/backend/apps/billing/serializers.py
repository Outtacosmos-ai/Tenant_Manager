from rest_framework import serializers
from .models import Invoice

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ['id', 'patient', 'date', 'amount', 'paid', 'payment_method', 'payment_date']
