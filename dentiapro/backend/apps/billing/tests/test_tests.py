import pytest
from decimal import Decimal
from datetime import datetime, timedelta
from django.utils import timezone
from django.core.exceptions import ValidationError
from rest_framework.exceptions import ErrorDetail

# Mocking dependencies if needed
from unittest.mock import Mock, patch

# Assuming these are your actual models and serializers
from apps.billing.models import Invoice, Patient, Appointment
from apps.billing.serializers import (
    InvoiceSerializer, 
    PatientSerializer, 
    AppointmentSerializer
)

@pytest.mark.django_db
class TestInvoiceSerializerValidation:
    def test_create_valid_invoice(self, create_patient, create_appointment):
        """
        Test creating a valid invoice with all required fields
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
        assert serializer.is_valid(raise_exception=False), serializer.errors
        invoice = serializer.save()

        # Verify saved data matches input
        assert invoice.invoice_number == 'INV-2023-001'
        assert invoice.amount == Decimal('100.50')
        assert invoice.status == 'draft'

    def test_invoice_amount_validation(self, create_patient, create_appointment):
        """
        Comprehensive test for invoice amount validation
        """
        patient = create_patient
        appointment = create_appointment
        
        test_cases = [
            # Invalid amounts
            {
                'amount': Decimal('-100.00'),
                'expected_error': 'Amount must be a positive value'
            },
            {
                'amount': Decimal('0.00'),
                'expected_error': 'Amount must be a positive value'
            },
            # Valid amount
            {
                'amount': Decimal('100.50'),
                'expected_error': None
            }
        ]

        for case in test_cases:
            data = {
                'patient': patient.id,
                'appointment': appointment.id,
                'invoice_number': 'INV-2023-TEST',
                'amount': case['amount'],
                'status': 'draft',
                'due_date': timezone.now().date() + timedelta(days=30)
            }

            serializer = InvoiceSerializer(data=data)
            
            if case['expected_error']:
                assert not serializer.is_valid()
                assert 'amount' in serializer.errors
            else:
                assert serializer.is_valid(), serializer.errors

    def test_invoice_status_choices(self, create_patient, create_appointment):
        """
        Test invoice status validation
        """
        patient = create_patient
        appointment = create_appointment
        
        # Valid statuses
        valid_statuses = ['draft', 'sent', 'paid', 'overdue', 'cancelled']
        
        # Invalid status
        invalid_status = 'invalid_status'

        # Test valid statuses
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
            assert serializer.is_valid(), f"Failed for valid status: {status}"

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
        Comprehensive due date validation test
        """
        patient = create_patient
        appointment = create_appointment
        
        test_cases = [
            # Past due date
            {
                'due_date': timezone.now().date() - timedelta(days=30),
                'should_be_valid': False
            },
            # Future due date
            {
                'due_date': timezone.now().date() + timedelta(days=30),
                'should_be_valid': True
            },
            # Today's date
            {
                'due_date': timezone.now().date(),
                'should_be_valid': True
            }
        ]

        for case in test_cases:
            data = {
                'patient': patient.id,
                'appointment': appointment.id,
                'invoice_number': 'INV-2023-DUEDATE',
                'amount': Decimal('100.50'),
                'status': 'draft',
                'due_date': case['due_date']
            }

            serializer = InvoiceSerializer(data=data)
            
            if case['should_be_valid']:
                assert serializer.is_valid(), f"Failed for due date: {case['due_date']}"
            else:
                assert not serializer.is_valid()
                assert 'due_date' in serializer.errors

@pytest.mark.django_db
class TestPatientSerializerValidation:
    def test_patient_creation_and_validation(self):
        """
        Comprehensive patient creation and validation test
        """
        test_cases = [
            # Valid patient data
            {
                'data': {
                    'first_name': 'John',
                    'last_name': 'Doe',
                    'email': 'john.doe@example.com',
                    'phone_number': '+1234567890'
                },
                'should_be_valid': True
            },
            # Invalid email formats
            {
                'data': {
                    'first_name': 'Invalid',
                    'last_name': 'Email',
                    'email': 'invalid-email',
                    'phone_number': '+1234567890'
                },
                'should_be_valid': False
            }
        ]

        for case in test_cases:
            serializer = PatientSerializer(data=case['data'])
            
            if case['should_be_valid']:
                assert serializer.is_valid(), serializer.errors
                patient = serializer.save()
                assert patient.first_name == case['data']['first_name']
            else:
                assert not serializer.is_valid()
                assert 'email' in serializer.errors

@pytest.mark.django_db
class TestAppointmentSerializerValidation:
    def test_appointment_creation_and_validation(self, create_patient):
        """
        Comprehensive appointment creation and validation test
        """
        patient = create_patient
        
        test_cases = [
            # Valid appointment
            {
                'data': {
                    'patient': patient.id,
                    'appointment_date': timezone.now() + timedelta(days=7),
                    'duration': 60,
                    'status': 'scheduled'
                },
                'should_be_valid': True
            },
            # Past appointment date
            {
                'data': {
                    'patient': patient.id,
                    'appointment_date': timezone.now() - timedelta(days=7),
                    'duration': 60,
                    'status': 'scheduled'
                },
                'should_be_valid': False
            }
        ]

        for case in test_cases:
            serializer = AppointmentSerializer(data=case['data'])
            
            if case['should_be_valid']:
                assert serializer.is_valid(), serializer.errors
                appointment = serializer.save()
                assert appointment.duration == case['data']['duration']
            else:
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