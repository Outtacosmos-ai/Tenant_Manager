from rest_framework import serializers
from .models import Cabinet

class CabinetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cabinet
        fields = [
            'id', 'tenant', 'name', 'description', 'address', 
            'contact_number', 'email', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate_contact_number(self, value):
        """Validate that the contact number is numeric and has the correct length."""
        if not value.isdigit() or len(value) < 10:
            raise serializers.ValidationError("Contact number must be numeric and at least 10 digits.")
        return value
