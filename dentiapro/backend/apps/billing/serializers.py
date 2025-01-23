from rest_framework import serializers
from .models import Invoice
from datetime import datetime

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ['id', 'patient', 'date', 'amount', 'paid', 'payment_method', 'payment_date', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
        extra_kwargs = {
            'payment_date': {'required': True},  # Ensure payment_date is always provided
            'amount': {'required': True},  # Ensure amount is always provided and positive
        }

    def validate_amount(self, value):
        """Ensure the amount is a positive value"""
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value

    def validate_payment_date(self, value):
        """Ensure the payment_date is not in the future"""
        if value > datetime.now().date():
            raise serializers.ValidationError("Payment date cannot be in the future.")
        return value
