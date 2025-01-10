from rest_framework import serializers
from .models import Patient

class PatientSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Patient
        fields = ['id', 'user', 'date_of_birth', 'address', 'phone_number', 'emergency_contact']

    def validate_phone_number(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Phone number must contain only digits.")
        if len(value) < 10:
            raise serializers.ValidationError("Phone number must be at least 10 digits long.")
        return value

    def validate_emergency_contact(self, value):
        if len(value.strip()) == 0:
            raise serializers.ValidationError("Emergency contact cannot be empty.")
        return value
