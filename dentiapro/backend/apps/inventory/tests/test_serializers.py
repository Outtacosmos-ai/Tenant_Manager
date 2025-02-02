# tests/test_inventory_serializers.py
import pytest
from rest_framework import serializers
from apps.tenant.models import Tenant
from apps.inventory.models import Category, InventoryItem
from apps.inventory.serializers import CategorySerializer, InventoryItemSerializer

@pytest.mark.django_db
def test_category_serializer():
    # Create a Tenant instance
    tenant = Tenant.objects.create(name="Test Tenant", description="Test Description")

    # Create a Category instance
    category = Category.objects.create(
        tenant=tenant,
        name="Test Category",
        description="Test Description"
    )

    # Serialize the Category instance
    serializer = CategorySerializer(category)
    serialized_data = serializer.data

    # Assert that the serialized data matches the expected output
    assert serialized_data['id'] == category.id
    assert serialized_data['name'] == "Test Category"
    assert serialized_data['description'] == "Test Description"
    assert 'created_at' in serialized_data  # read-only field
    assert 'updated_at' in serialized_data  # read-only field

@pytest.mark.django_db
def test_category_serializer_read_only_fields():
    # Data for creating a Category instance
    category_data = {
        "name": "Test Category",
        "description": "Test Description",
        "created_at": "2023-01-01T00:00:00Z",  # Attempt to set read-only field
        "updated_at": "2023-01-01T00:00:00Z"   # Attempt to set read-only field
    }

    # Deserialize the data
    serializer = CategorySerializer(data=category_data)
    assert serializer.is_valid(), serializer.errors

    # Save the deserialized data
    category = serializer.save()

    # Assert that read-only fields are not set by the input data
    assert category.created_at != "2023-01-01T00:00:00Z"
    assert category.updated_at != "2023-01-01T00:00:00Z"

@pytest.mark.django_db
def test_inventory_item_serializer():
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

    # Serialize the InventoryItem instance
    serializer = InventoryItemSerializer(inventory_item)
    serialized_data = serializer.data

    # Assert that the serialized data matches the expected output
    assert serialized_data['id'] == inventory_item.id
    assert serialized_data['name'] == "Test Item"
    assert serialized_data['category']['id'] == category.id  # Nested CategorySerializer
    assert serialized_data['category_id'] == category.id     # Write-only field
    assert serialized_data['description'] == "Test Description"
    assert serialized_data['quantity'] == 10
    assert serialized_data['unit'] == "pieces"
    assert serialized_data['minimum_quantity'] == 5
    assert serialized_data['cost_price'] == "9.99"
    assert 'created_at' in serialized_data  # read-only field
    assert 'updated_at' in serialized_data  # read-only field

@pytest.mark.django_db
def test_inventory_item_serializer_create():
    # Create a Tenant instance
    tenant = Tenant.objects.create(name="Test Tenant", description="Test Description")

    # Create a Category instance
    category = Category.objects.create(tenant=tenant, name="Test Category")

    # Data for creating an InventoryItem instance
    inventory_item_data = {
        "name": "Test Item",
        "category_id": category.id,
        "description": "Test Description",
        "quantity": 10,
        "unit": "pieces",
        "minimum_quantity": 5,
        "cost_price": 9.99
    }

    # Deserialize the data
    serializer = InventoryItemSerializer(data=inventory_item_data)
    assert serializer.is_valid(), serializer.errors

    # Save the deserialized data
    inventory_item = serializer.save(tenant=tenant)

    # Assert that the InventoryItem instance was created correctly
    assert inventory_item.tenant == tenant
    assert inventory_item.category == category
    assert inventory_item.name == "Test Item"
    assert inventory_item.description == "Test Description"
    assert inventory_item.quantity == 10
    assert inventory_item.unit == "pieces"
    assert inventory_item.minimum_quantity == 5
    assert inventory_item.cost_price == 9.99

@pytest.mark.django_db
def test_inventory_item_serializer_validate_quantity():
    # Data with invalid quantity (negative value)
    invalid_data = {
        "name": "Test Item",
        "category_id": 1,  # Assuming a valid category ID exists
        "description": "Test Description",
        "quantity": -10,  # Invalid: negative quantity
        "unit": "pieces",
        "minimum_quantity": 5,
        "cost_price": 9.99
    }

    # Attempt to deserialize invalid data
    serializer = InventoryItemSerializer(data=invalid_data)
    assert not serializer.is_valid()
    assert 'quantity' in serializer.errors
    assert "Quantity cannot be negative." in str(serializer.errors['quantity'])

@pytest.mark.django_db
def test_inventory_item_serializer_validate_cost_price():
    # Data with invalid cost_price (negative value)
    invalid_data = {
        "name": "Test Item",
        "category_id": 1,  # Assuming a valid category ID exists
        "description": "Test Description",
        "quantity": 10,
        "unit": "pieces",
        "minimum_quantity": 5,
        "cost_price": -9.99  # Invalid: negative cost_price
    }

    # Attempt to deserialize invalid data
    serializer = InventoryItemSerializer(data=invalid_data)
    assert not serializer.is_valid()
    assert 'cost_price' in serializer.errors
    assert "Cost price cannot be negative." in str(serializer.errors['cost_price'])

@pytest.mark.django_db
def test_inventory_item_serializer_missing_required_fields():
    # Data with missing required fields
    invalid_data = {
        "name": "Test Item",
        "description": "Test Description",
        "quantity": 10,
        "unit": "pieces",
        "minimum_quantity": 5,
        "cost_price": 9.99
    }

    # Attempt to deserialize invalid data
    serializer = InventoryItemSerializer(data=invalid_data)
    assert not serializer.is_valid()
    assert 'category_id' in serializer.errors  # 'category_id' is a required field