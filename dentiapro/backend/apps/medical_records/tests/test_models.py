# tests/test_medical_record_models.py
import pytest
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from apps.tenant.models import Tenant
from apps.users.models import User
from apps.medical_records.models import MedicalRecord

@pytest.mark.django_db
def test_medical_record_model():
    # Create a Tenant instance
    tenant = Tenant.objects.create(name="Test Tenant", description="Test Description")

    # Create a Patient instance
    patient = User.objects.create_user(username="patient1", password="testpass123")

    # Create a Dentist instance
    dentist = User.objects.create_user(username="dentist1", password="testpass123")

    # Create a MedicalRecord instance
    medical_record = MedicalRecord.objects.create(
        tenant=tenant,
        patient=patient,
        dentist=dentist,
        diagnosis="Cavity",
        treatment_plan="Fill the cavity",
        notes="Patient has a history of cavities.",
        attachments=None
    )

    # Retrieve the MedicalRecord instance from the database
    saved_record = MedicalRecord.objects.get(id=medical_record.id)

    # Assert that the MedicalRecord instance was saved correctly
    assert saved_record.tenant == tenant
    assert saved_record.patient == patient
    assert saved_record.dentist == dentist
    assert saved_record.diagnosis == "Cavity"
    assert saved_record.treatment_plan == "Fill the cavity"
    assert saved_record.notes == "Patient has a history of cavities."
    assert saved_record.attachments is None
    assert saved_record.created_at is not None
    assert saved_record.updated_at is not None

    # Test the __str__ method
    assert str(saved_record) == f"Medical Record for {patient} on {saved_record.created_at.date()}"

    # Test the Meta options
    assert saved_record._meta.db_table == "medical_records"
    assert saved_record._meta.ordering == ["-created_at"]
    assert saved_record._meta.verbose_name == "Medical Record"
    assert saved_record._meta.verbose_name_plural == "Medical Records"

@pytest.mark.django_db
def test_medical_record_model_required_fields():
    # Create a Tenant instance
    tenant = Tenant.objects.create(name="Test Tenant", description="Test Description")

    # Create a Patient instance
    patient = User.objects.create_user(username="patient1", password="testpass123")

    # Create a Dentist instance
    dentist = User.objects.create_user(username="dentist1", password="testpass123")

    # Test that the 'tenant' field is required
    with pytest.raises(IntegrityError):
        MedicalRecord.objects.create(
            patient=patient,
            dentist=dentist,
            diagnosis="Cavity",
            treatment_plan="Fill the cavity"
        )

    # Test that the 'patient' field is required
    with pytest.raises(IntegrityError):
        MedicalRecord.objects.create(
            tenant=tenant,
            dentist=dentist,
            diagnosis="Cavity",
            treatment_plan="Fill the cavity"
        )

    # Test that the 'dentist' field is required
    with pytest.raises(IntegrityError):
        MedicalRecord.objects.create(
            tenant=tenant,
            patient=patient,
            diagnosis="Cavity",
            treatment_plan="Fill the cavity"
        )

    # Test that the 'diagnosis' field is required
    with pytest.raises(IntegrityError):
        MedicalRecord.objects.create(
            tenant=tenant,
            patient=patient,
            dentist=dentist,
            treatment_plan="Fill the cavity"
        )

    # Test that the 'treatment_plan' field is required
    with pytest.raises(IntegrityError):
        MedicalRecord.objects.create(
            tenant=tenant,
            patient=patient,
            dentist=dentist,
            diagnosis="Cavity"
        )

@pytest.mark.django_db
def test_medical_record_model_attachments_optional():
    # Create a Tenant instance
    tenant = Tenant.objects.create(name="Test Tenant", description="Test Description")

    # Create a Patient instance
    patient = User.objects.create_user(username="patient1", password="testpass123")

    # Create a Dentist instance
    dentist = User.objects.create_user(username="dentist1", password="testpass123")

    # Create a MedicalRecord instance without attachments
    medical_record = MedicalRecord.objects.create(
        tenant=tenant,
        patient=patient,
        dentist=dentist,
        diagnosis="Cavity",
        treatment_plan="Fill the cavity"
    )

    # Assert that attachments are optional
    assert medical_record.attachments is None

@pytest.mark.django_db
def test_medical_record_model_ordering():
    # Create a Tenant instance
    tenant = Tenant.objects.create(name="Test Tenant", description="Test Description")

    # Create a Patient instance
    patient = User.objects.create_user(username="patient1", password="testpass123")

    # Create a Dentist instance
    dentist = User.objects.create_user(username="dentist1", password="testpass123")

    # Create multiple MedicalRecord instances
    record1 = MedicalRecord.objects.create(
        tenant=tenant,
        patient=patient,
        dentist=dentist,
        diagnosis="Cavity",
        treatment_plan="Fill the cavity"
    )
    record2 = MedicalRecord.objects.create(
        tenant=tenant,
        patient=patient,
        dentist=dentist,
        diagnosis="Gingivitis",
        treatment_plan="Prescribe mouthwash"
    )

    # Retrieve records and assert ordering
    records = MedicalRecord.objects.all()
    assert records[0] == record2  # Most recent first
    assert records[1] == record1