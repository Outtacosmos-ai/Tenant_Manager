import pytest
from decimal import Decimal
from django.utils import timezone
from django.core.exceptions import ValidationError
from apps.billing.models import Invoice
from apps.tenant.models import Tenant
from apps.users.models import User
from apps.appointments.models import Appointment

@pytest.mark.django_db
def test_create_invoice():
    # Create necessary related objects
    tenant = Tenant.objects.create(name="Test Tenant")
    patient = User.objects.create(username="testpatient")
    appointment = Appointment.objects.create(
        tenant=tenant, 
        patient=patient
    )

    # Create an invoice
    invoice = Invoice.objects.create(
        tenant=tenant,
        patient=patient,
        appointment=appointment,
        invoice_number="INV-2023-001",
        amount=Decimal('100.50'),
        status='draft',
        due_date=timezone.now().date(),
        notes="Test invoice"
    )

    # Assertions
    assert invoice.tenant == tenant
    assert invoice.patient == patient
    assert invoice.appointment == appointment
    assert invoice.invoice_number == "INV-2023-001"
    assert invoice.amount == Decimal('100.50')
    assert invoice.status == 'draft'
    assert invoice.notes == "Test invoice"
    assert invoice.created_at is not None
    assert invoice.updated_at is not None

@pytest.mark.django_db
def test_invoice_status_choices():
    tenant = Tenant.objects.create(name="Test Tenant")
    patient = User.objects.create(username="testpatient")

    # Test valid status choices
    valid_statuses = ['draft', 'sent', 'paid', 'overdue', 'cancelled']
    
    for status in valid_statuses:
        invoice = Invoice.objects.create(
            tenant=tenant,
            patient=patient,
            invoice_number=f"INV-{status}",
            amount=Decimal('100.00'),
            status=status,
            due_date=timezone.now().date()
        )
        assert invoice.status == status

@pytest.mark.django_db
def test_invoice_unique_invoice_number():
    tenant = Tenant.objects.create(name="Test Tenant")
    patient = User.objects.create(username="testpatient")

    # Create first invoice
    Invoice.objects.create(
        tenant=tenant,
        patient=patient,
        invoice_number="INV-UNIQUE-001",
        amount=Decimal('100.00'),
        status='draft',
        due_date=timezone.now().date()
    )

    # Try to create another invoice with same invoice number (should raise exception)
    with pytest.raises(Exception):
        Invoice.objects.create(
            tenant=tenant,
            patient=patient,
            invoice_number="INV-UNIQUE-001",
            amount=Decimal('200.00'),
            status='draft',
            due_date=timezone.now().date()
        )

@pytest.mark.django_db
def test_invoice_meta_options():
    # Check Meta options
    assert Invoice._meta.db_table == 'invoices'
    assert Invoice._meta.ordering == ['-created_at']

@pytest.mark.django_db
def test_invoice_optional_fields():
    tenant = Tenant.objects.create(name="Test Tenant")
    patient = User.objects.create(username="testpatient")

    # Create invoice with optional fields as None/blank
    invoice = Invoice.objects.create(
        tenant=tenant,
        patient=patient,
        invoice_number="INV-OPTIONAL-001",
        amount=Decimal('150.75'),
        status='draft',
        due_date=timezone.now().date(),
        appointment=None,
        notes=""
    )

    assert invoice.appointment is None
    assert invoice.notes == ""

@pytest.mark.django_db
def test_invoice_amount_validation():
    tenant = Tenant.objects.create(name="Test Tenant")
    patient = User.objects.create(username="testpatient")

    # Test decimal places and max digits
    invoice = Invoice.objects.create(
        tenant=tenant,
        patient=patient,
        invoice_number="INV-AMOUNT-001",
        amount=Decimal('9999999.99'),  # Maximum allowed
        status='draft',
        due_date=timezone.now().date()
    )

    assert invoice.amount == Decimal('9999999.99')

    # Test amount with more than 2 decimal places (should raise validation error)
    with pytest.raises(ValidationError):
        Invoice.objects.create(
            tenant=tenant,
            patient=patient,
            invoice_number="INV-AMOUNT-002",
            amount=Decimal('100.999'),  # More than 2 decimal places
            status='draft',
            due_date=timezone.now().date()
        )