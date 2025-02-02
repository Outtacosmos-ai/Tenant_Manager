# tests/test_inventory_models.py
import pytest
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from apps.tenant.models import Tenant
from apps.inventory.models import Cabinet

@pytest.mark.django_db
def test_cabinet_model():
    # Create a Tenant instance
    tenant = Tenant.objects.create(name="Test Tenant", description="Test Description")

    # Create a Cabinet instance
    cabinet = Cabinet.objects.create(
        tenant=tenant,
        name="Test Cabinet",
        description="Test Description",
        address="123 Test St",
        contact_number="1234567890",
        email="test@example.com",
        is_active=True
    )

    # Retrieve the Cabinet instance from the database
    saved_cabinet = Cabinet.objects.get(id=cabinet.id)

    # Assert that the Cabinet instance was saved correctly
    assert saved_cabinet.tenant == tenant
    assert saved_cabinet.name == "Test Cabinet"
    assert saved_cabinet.description == "Test Description"
    assert saved_cabinet.address == "123 Test St"
    assert saved_cabinet.contact_number == "1234567890"
    assert saved_cabinet.email == "test@example.com"
    assert saved_cabinet.is_active is True
    assert saved_cabinet.created_at is not None
    assert saved_cabinet.updated_at is not None

    # Test the __str__ method
    assert str(saved_cabinet) == "Test Cabinet"

    # Test the Meta options
    assert saved_cabinet._meta.db_table == 'cabinets'
    assert saved_cabinet._meta.ordering == ['name']

@pytest.mark.django_db
def test_cabinet_model_required_fields():
    # Create a Tenant instance
    tenant = Tenant.objects.create(name="Test Tenant", description="Test Description")

    # Test that the 'name' field is required
    with pytest.raises(IntegrityError):
        Cabinet.objects.create(tenant=tenant)

    # Test that the 'tenant' field is required
    with pytest.raises(IntegrityError):
        Cabinet.objects.create(name="Test Cabinet")

@pytest.mark.django_db
def test_cabinet_model_max_lengths():
    # Create a Tenant instance
    tenant = Tenant.objects.create(name="Test Tenant", description="Test Description")

    # Test max length for 'name' field
    with pytest.raises(ValidationError):
        cabinet = Cabinet(
            tenant=tenant,
            name="A" * 101,  # Exceeds max_length of 100
            description="Test Description"
        )
        cabinet.full_clean()

    # Test max length for 'contact_number' field
    with pytest.raises(ValidationError):
        cabinet = Cabinet(
            tenant=tenant,
            name="Test Cabinet",
            contact_number="1" * 16  # Exceeds max_length of 15
        )
        cabinet.full_clean()