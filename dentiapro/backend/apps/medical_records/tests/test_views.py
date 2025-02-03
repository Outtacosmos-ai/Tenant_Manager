import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from medical_records.models import MedicalRecord
from medical_records.serializers import MedicalRecordSerializer

@pytest.mark.django_db
def test_medical_record_list_as_patient():
    client = APIClient()
    patient = get_user_model().objects.create_user(username='patient', password='testpass', role='patient')
    client.force_authenticate(user=patient)
    response = client.get('/medical-records/')
    assert response.status_code == 200

@pytest.mark.django_db
def test_medical_record_list_as_dentist():
    client = APIClient()
    dentist = get_user_model().objects.create_user(username='dentist', password='testpass', role='dentist')
    client.force_authenticate(user=dentist)
    response = client.get('/medical-records/')
    assert response.status_code == 200

@pytest.mark.django_db
def test_medical_record_create():
    client = APIClient()
    admin = get_user_model().objects.create_user(username='admin', password='testpass', is_tenant_admin=True)
    client.force_authenticate(user=admin)
    data = {
        "diagnosis": "Tooth decay",
        "treatment_plan": "Fill cavity",
        "notes": "Patient is sensitive to anesthesia."
    }
    response = client.post('/medical-records/', data)
    assert response.status_code == 201
