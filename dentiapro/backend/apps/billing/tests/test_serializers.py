import pytest
from decimal import Decimal
from datetime import datetime, timedelta
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

# Assuming these are your actual models and serializers
from apps.billing.models import Invoice, Patient, Appointment
from apps.billing.serializers import (
    InvoiceSerializer, 
    PatientSerializer, 
    AppointmentSerializer
)

@pytest.mark.django_db
class TestInvoiceSerializer:
    def test_create_valid_invoice(self, create_patient, create_appointment):
        """
        Test creating a valid invoice
        """
        patient = create_patient
        appointment = create_appointment
        
        valid_data = {
            'patient': patient.id,
            'appointment': appointment.id,
            'invoice_number': 'INV-2023-001',
            'amount': Decimal('100.50'),
            'status': 'draft',
            'due_date': timezone.now().date() + timedelta(days=30)
        }

        serializer = InvoiceSerializer(data=valid_data)
        assert serializer.is_valid(), serializer.errors
        invoice = serializer.save()

        assert invoice.invoice_number == 'INV-2023-001'
        assert invoice.amount == Decimal('100.50')
        assert invoice.status == 'draft'

    def test_invalid_invoice_amount(self, create_patient, create_appointment):
        """
        Test invoice creation with invalid amount
        """
        patient = create_patient
        appointment = create_appointment
        
        invalid_amounts = [
            Decimal('-100.00'),
            Decimal('0.00'),
            -50
        ]

        for amount in invalid_amounts:
            invalid_data = {
                'patient': patient.id,
                'appointment': appointment.id,
                'invoice_number': 'INV-2023-002',
                'amount': amount,
                'status': 'draft',
                'due_date': timezone.now().date() + timedelta(days=30)
            }

            serializer = InvoiceSerializer(data=invalid_data)
            assert not serializer.is_valid()
            assert 'amount' in serializer.errors

    def test_invoice_status_choices(self, create_patient, create_appointment):
        """
        Test valid and invalid invoice statuses
        """
        patient = create_patient
        appointment = create_appointment
        
        valid_statuses = ['draft', 'sent', 'paid', 'overdue', 'cancelled']
        invalid_status = 'invalid_status'

        for status in valid_statuses:
            valid_data = {
                'patient': patient.id,
                'appointment': appointment.id,
                'invoice_number': f'INV-2023-{status}',
                'amount': Decimal('100.50'),
                'status': status,
                'due_date': timezone.now().date() + timedelta(days=30)
            }

            serializer = InvoiceSerializer(data=valid_data)
            assert serializer.is_valid(), f"Failed for status: {status}"

        # Test invalid status
        invalid_data = {
            'patient': patient.id,
            'appointment': appointment.id,
            'invoice_number': 'INV-2023-INVALID',
            'amount': Decimal('100.50'),
            'status': invalid_status,
            'due_date': timezone.now().date() + timedelta(days=30)
        }

        serializer = InvoiceSerializer(data=invalid_data)
        assert not serializer.is_valid()
        assert 'status' in serializer.errors

    def test_invoice_due_date_validation(self, create_patient, create_appointment):
        """
        Test due date validation
        """
        patient = create_patient
        appointment = create_appointment
        
        # Past due date
        past_due_date = timezone.now().date() - timedelta(days=30)
        invalid_data = {
            'patient': patient.id,
            'appointment': appointment.id,
            'invoice_number': 'INV-2023-PAST',
            'amount': Decimal('100.50'),
            'status': 'draft',
            'due_date': past_due_date
        }

        serializer = InvoiceSerializer(data=invalid_data)
        assert not serializer.is_valid()
        assert 'due_date' in serializer.errors

@pytest.mark.django_db
class TestPatientSerializer:
    def test_create_valid_patient(self):
        """
        Test creating a valid patient
        """
        valid_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'phone_number': '+1234567890'
        }

        serializer = PatientSerializer(data=valid_data)
        assert serializer.is_valid(), serializer.errors
        patient = serializer.save()

        assert patient.first_name == 'John'
        assert patient.last_name == 'Doe'

    def test_patient_email_validation(self):
        """
        Test patient email validation
        """
        invalid_emails = [
            'invalid-email',
            'missing@domain',
            '@incomplete.com'
        ]

        for email in invalid_emails:
            invalid_data = {
                'first_name': 'John',
                'last_name': 'Doe',
                'email': email,
                'phone_number': '+1234567890'
            }

            serializer = PatientSerializer(data=invalid_data)
            assert not serializer.is_valid()
            assert 'email' in serializer.errors

@pytest.mark.django_db
class TestAppointmentSerializer:
    def test_create_valid_appointment(self, create_patient):
        """
        Test creating a valid appointment
        """
        patient = create_patient
        
        valid_data = {
            'patient': patient.id,
            'appointment_date': timezone.now() + timedelta(days=7),
            'duration': 60,
            'status': 'scheduled'
        }

        serializer = AppointmentSerializer(data=valid_data)
        assert serializer.is_valid(), serializer.errors
        appointment = serializer.save()

        assert appointment.patient == patient
        assert appointment.duration == 60

    def test_appointment_past_date_validation(self, create_patient):
        """
        Test appointment date validation
        """
        patient = create_patient
        
        past_date = timezone.now() - timedelta(days=7)
        invalid_data = {
            'patient': patient.id,
            'appointment_date': past_date,
            'duration': 60,
            'status': 'scheduled'
        }

        serializer = AppointmentSerializer(data=invalid_data)
        assert not serializer.is_valid()
        assert 'appointment_date' in serializer.errors

# Fixtures for creating test data
@pytest.fixture
def create_patient():
    """
    Fixture to create a patient for testing
    """
    return Patient.objects.create(
        first_name='Test',
        last_name='Patient',
        email='test.patient@example.com',
        phone_number='+1234567890'
    )

@pytest.fixture
def create_appointment(create_patient):
    """
    Fixture to create an appointment for testing
    """
    return Appointment.objects.create(
        patient=create_patient,
        appointment_date=timezone.now() + timedelta(days=7),
        duration=60,
        status='scheduled'
    )