from rest_framework import serializers
from .models import Prescription

class PrescriptionSerializer(serializers.ModelSerializer):
    patient = serializers.StringRelatedField()
    dentist = serializers.StringRelatedField()

    class Meta:
        model = Prescription
        fields = ['id', 'patient', 'dentist', 'date', 'medication', 'dosage', 'frequency', 'duration', 'notes', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
        extra_kwargs = {
            'date': {'required': True},  # Ensure the prescription date is always provided
            'medication': {'required': True},  # Ensure medication is always provided
            'dosage': {'required': True},  # Ensure dosage is provided
            'frequency': {'required': True},  # Ensure frequency is provided
            'duration': {'required': True},  # Ensure duration is provided
        }

    def validate_date(self, value):
        """Ensure the prescription date is not in the future"""
        if value > datetime.now().date():
            raise serializers.ValidationError("Prescription date cannot be in the future.")
        return value
