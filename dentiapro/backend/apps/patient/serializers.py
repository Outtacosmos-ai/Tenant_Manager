from rest_framework import serializers
from .models import Patient

class PatientSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Patient
        fields = ['id', 'user', 'date_of_birth', 'address', 'phone', 'emergency_contact', 'medical_history']

