from rest_framework import serializers
from .models import MedicalRecord
from datetime import datetime


class MedicalRecordSerializer(serializers.ModelSerializer):
    patient = serializers.StringRelatedField(read_only=True)
    dentist = serializers.StringRelatedField(read_only=True)
    attachments = serializers.FileField(allow_null=True, required=False)

    class Meta:
        model = MedicalRecord
        fields = [
            'id',
            'tenant',
            'patient',
            'dentist',
            'diagnosis',
            'treatment_plan',
            'notes',
            'attachments',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']
        extra_kwargs = {
            'diagnosis': {'required': True},
            'treatment_plan': {'required': True},
        }

    def validate_diagnosis(self, value):
        if not value.strip():
            raise serializers.ValidationError("Diagnosis cannot be empty.")
        return value

    def validate_treatment_plan(self, value):
        if not value.strip():
            raise serializers.ValidationError("Treatment plan cannot be empty.")
        return value

    def validate_notes(self, value):
        if value and len(value) > 1000:
            raise serializers.ValidationError("Notes cannot exceed 1000 characters.")
        return value

    def validate(self, data):
        if data.get('attachments') and not data['attachments'].name.endswith(('.pdf', '.doc', '.docx')):
            raise serializers.ValidationError("Attachments must be a PDF or Word document.")
        return data
