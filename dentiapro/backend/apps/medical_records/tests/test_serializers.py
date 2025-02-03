import pytest
from medical_records.serializers import MedicalRecordSerializer
from medical_records.models import MedicalRecord
from django.core.files.uploadedfile import SimpleUploadedFile

def test_valid_medical_record_serializer():
    data = {
        'diagnosis': 'Cavity in molar',
        'treatment_plan': 'Fill the cavity with composite resin.',
        'notes': 'Patient experiences mild sensitivity.',
        'attachments': None
    }
    serializer = MedicalRecordSerializer(data=data)
    assert serializer.is_valid(), serializer.errors

def test_missing_required_fields():
    data = {
        'notes': 'This is a test note.'  # Missing diagnosis and treatment_plan
    }
    serializer = MedicalRecordSerializer(data=data)
    assert not serializer.is_valid()
    assert 'diagnosis' in serializer.errors
    assert 'treatment_plan' in serializer.errors

def test_empty_diagnosis():
    data = {
        'diagnosis': ' ',  # Invalid empty diagnosis
        'treatment_plan': 'Standard cleaning',
    }
    serializer = MedicalRecordSerializer(data=data)
    assert not serializer.is_valid()
    assert 'diagnosis' in serializer.errors

def test_empty_treatment_plan():
    data = {
        'diagnosis': 'Gum infection',
        'treatment_plan': ' ',  # Invalid empty treatment plan
    }
    serializer = MedicalRecordSerializer(data=data)
    assert not serializer.is_valid()
    assert 'treatment_plan' in serializer.errors

def test_notes_character_limit():
    data = {
        'diagnosis': 'Tooth decay',
        'treatment_plan': 'Root canal',
        'notes': 'a' * 1001  # Exceeds 1000 character limit
    }
    serializer = MedicalRecordSerializer(data=data)
    assert not serializer.is_valid()
    assert 'notes' in serializer.errors

def test_valid_attachment():
    file = SimpleUploadedFile("test.pdf", b"dummy data", content_type="application/pdf")
    data = {
        'diagnosis': 'Fractured tooth',
        'treatment_plan': 'Extraction',
        'attachments': file
    }
    serializer = MedicalRecordSerializer(data=data)
    assert serializer.is_valid(), serializer.errors

def test_invalid_attachment_format():
    file = SimpleUploadedFile("image.jpg", b"dummy data", content_type="image/jpeg")
    data = {
        'diagnosis': 'Gingivitis',
        'treatment_plan': 'Deep cleaning',
        'attachments': file
    }
    serializer = MedicalRecordSerializer(data=data)
    assert not serializer.is_valid()
    assert 'attachments' in serializer.errors
