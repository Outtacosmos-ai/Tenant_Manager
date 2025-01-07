from rest_framework import serializers
from .models import Prescription

class PrescriptionSerializer(serializers.ModelSerializer):
    patient = serializers.StringRelatedField()
    dentist = serializers.StringRelatedField()

    class Meta:
        model = Prescription
        fields = ['id', 'patient', 'dentist', 'date', 'medication', 'dosage', 'frequency', 'duration', 'notes']
