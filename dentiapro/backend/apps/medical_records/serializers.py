from rest_framework import serializers
from .models import MedicalRecord

class MedicalRecordSerializer(serializers.ModelSerializer):
    patient = serializers.StringRelatedField()
    dentist = serializers.StringRelatedField()

    class Meta:
        model = MedicalRecord
        fields = ['id', 'patient', 'dentist', 'date', 'diagnosis', 'treatment', 'notes']