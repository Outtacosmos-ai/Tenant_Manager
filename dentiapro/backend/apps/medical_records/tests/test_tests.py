import pytest
from django.utils import timezone
from medical_records.models import MedicalRecord
from apps.tenant.models import Tenant
from apps.users.models import User

@pytest.mark.django_db
def test_medical_record_creation():
    # Create tenant
    tenant = Tenant.objects.create(name="Tenant 1")

    # Create users
    patient = User.objects.create_user(username='patient', password='testpass123')
    dentist = User.objects.create_user(username='dentist', password='testpass123')

    # Create medical record
    medical_record = MedicalRecord.objects.create(
        tenant=tenant,
        patient=patient,
        dentist=dentist,
        diagnosis='Tooth decay',
        treatment_plan='Fill cavity',
        notes='Patient is sensitive to anesthesia.',
        created_at=timezone.now()
    )

    assert medical_record.diagnosis == 'Tooth decay'
    assert medical_record.treatment_plan == 'Fill cavity'
    assert medical_record.tenant == tenant

@pytest.mark.django_db
def test_medical_record_str_representation():
    tenant = Tenant.objects.create(name="Tenant 1")
    patient = User.objects.create_user(username='patient', password='testpass123')
    dentist = User.objects.create_user(username='dentist', password='testpass123')
    medical_record = MedicalRecord.objects.create(
        tenant=tenant,
        patient=patient,
        dentist=dentist,
        diagnosis='Tooth decay',
        treatment_plan='Fill cavity',
        notes='Patient is sensitive to anesthesia.',
        created_at=timezone.now()
    )
    assert str(medical_record) == f"Medical Record for {patient} - {medical_record.created_at.date()}"
