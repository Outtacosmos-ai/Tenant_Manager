# tests/test_inventory_models.py
import pytest
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from apps.tenant.models import Tenant
from apps.inventory.models import Category, InventoryItem

@pytest.mark.django_db
def test_category_model():
    # Create a Tenant instance
    tenant = Tenant.objects.create(name="Test Tenant", description="Test Description")

    # Create a Category instance
    category = Category.objects.create(
        tenant=tenant,
        name="Test Category",
        description="Test Description"
    )

    # Retrieve the Category instance from the database
    saved_category = Category.objects.get(id=category.id)

    # Assert that the Category instance was saved correctly
    assert saved_category.tenant == tenant
    assert saved_category.name == "Test Category"
    assert saved_category.description == "Test Description"
    assert saved_category.created_at is not None
    assert saved_category.updated_at is not None

    # Test the __str__ method
    assert str(saved_category) == "Test Category"

    # Test the Meta options
    assert saved_category._meta.db_table == "categories"
    assert saved_category._meta.ordering == ["name"]

@pytest.mark.django_db
def test_category_model_unique_name():
    # Create a Tenant instance
    tenant = Tenant.objects.create(name="Test Tenant", description="Test Description")

    # Create a Category instance
    Category.objects.create(tenant=tenant, name="Test Category")

    # Attempt to create another Category with the same name (should raise IntegrityError)
    with pytest.raises(IntegrityError):
        Category.objects.create(tenant=tenant, name="Test Category")

@pytest.mark.django_db
def test_inventory_item_model():
    # Create a Tenant instance
    tenant = Tenant.objects.create(name="Test Tenant", description="Test Description")

    # Create a Category instance
    category = Category.objects.create(tenant=tenant, name="Test Category")

    # Create an InventoryItem instance
    inventory_item = InventoryItem.objects.create(
        tenant=tenant,
        category=category,
        name="Test Item",
        description="Test Description",
        quantity=10,
        unit="pieces",
        minimum_quantity=5,
        cost_price=9.99
    )

    # Retrieve the InventoryItem instance from the database
    saved_item = InventoryItem.objects.get(id=inventory_item.id)

    # Assert that the InventoryItem instance was saved correctly
    assert saved_item.tenant == tenant
    assert saved_item.category == category
    assert saved_item.name == "Test Item"
    assert saved_item.description == "Test Description"
    assert saved_item.quantity == 10
    assert saved_item.unit == "pieces"
    assert saved_item.minimum_quantity == 5
    assert saved_item.cost_price == 9.99
    assert saved_item.created_at is not None
    assert saved_item.updated_at is not None

    # Test the __str__ method
    assert str(saved_item) == "Test Item (10 pieces)"

    # Test the Meta options
    assert saved_item._meta.db_table == "inventory_items"
    assert saved_item._meta.ordering == ["name"]

@pytest.mark.django_db
def test_inventory_item_model_without_category():
    # Create a Tenant instance
    tenant = Tenant.objects.create(name="Test Tenant", description="Test Description")

    # Create an InventoryItem instance without a category
    inventory_item = InventoryItem.objects.create(
        tenant=tenant,
        name="Test Item",
        description="Test Description",
        quantity=10,
        unit="pieces",
        minimum_quantity=5,
        cost_price=9.99
    )

    # Retrieve the InventoryItem instance from the database
    saved_item = InventoryItem.objects.get(id=inventory_item.id)

    # Assert that the category is None
    assert saved_item.category is None

@pytest.mark.django_db
def test_inventory_item_model_required_fields():
    # Create a Tenant instance
    tenant = Tenant.objects.create(name="Test Tenant", description="Test Description")

    # Test that the 'name' field is required
    with pytest.raises(IntegrityError):
        InventoryItem.objects.create(tenant=tenant)

    # Test that the 'tenant' field is required
    with pytest.raises(IntegrityError):
        InventoryItem.objects.create(name="Test Item")

@pytest.mark.django_db
def test_inventory_item_model_quantity_validation():
    # Create a Tenant instance
    tenant = Tenant.objects.create(name="Test Tenant", description="Test Description")

    # Attempt to create an InventoryItem with negative quantity (should raise ValidationError)
    with pytest.raises(ValidationError):
        item = InventoryItem(
            tenant=tenant,
            name="Test Item",
            quantity=-10,  # Invalid: negative quantity
            unit="pieces",
            cost_price=9.99
        )
        item.full_clean()

@pytest.mark.django_db
def test_inventory_item_model_minimum_quantity_validation():
    # Create a Tenant instance
    tenant = Tenant.objects.create(name="Test Tenant", description="Test Description")

    # Attempt to create an InventoryItem with negative minimum_quantity (should raise ValidationError)
    with pytest.raises(ValidationError):
        item = InventoryItem(
            tenant=tenant,
            name="Test Item",
            quantity=10,
            unit="pieces",
            minimum_quantity=-5,  # Invalid: negative minimum_quantity
            cost_price=9.99
        )
        item.full_clean()