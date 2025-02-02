# tests/test_inventory_models_pytest.py
import pytest
from decimal import Decimal
from django.core.exceptions import ValidationError
from apps.inventory.models import Category, InventoryItem

@pytest.mark.django_db
def test_inventory_item_creation():
    # Create a Category instance
    category = Category.objects.create(name='Dental Tools', description='Tools used in dental procedures')

    # Create an InventoryItem instance
    item = InventoryItem.objects.create(
        name='Dental Mirror',
        category=category,
        quantity=100,
        unit_price=Decimal('5.99'),
        reorder_level=20
    )

    # Assert that the item is an instance of InventoryItem
    assert isinstance(item, InventoryItem)

    # Test the __str__ method
    assert str(item) == 'Dental Mirror'

    # Test the category relationship
    assert item.category == category

    # Test the fields
    assert item.name == 'Dental Mirror'
    assert item.quantity == 100
    assert item.unit_price == Decimal('5.99')
    assert item.reorder_level == 20

@pytest.mark.django_db
def test_inventory_item_required_fields():
    # Create a Category instance
    category = Category.objects.create(name='Dental Tools', description='Tools used in dental procedures')

    # Test that the 'name' field is required
    with pytest.raises(ValidationError):
        item = InventoryItem(
            category=category,
            quantity=100,
            unit_price=Decimal('5.99'),
            reorder_level=20
        )
        item.full_clean()  # Triggers validation

    # Test that the 'category' field is required
    with pytest.raises(ValidationError):
        item = InventoryItem(
            name='Dental Mirror',
            quantity=100,
            unit_price=Decimal('5.99'),
            reorder_level=20
        )
        item.full_clean()  # Triggers validation

@pytest.mark.django_db
def test_inventory_item_quantity_validation():
    # Create a Category instance
    category = Category.objects.create(name='Dental Tools', description='Tools used in dental procedures')

    # Test that the 'quantity' field cannot be negative
    with pytest.raises(ValidationError):
        item = InventoryItem(
            name='Dental Mirror',
            category=category,
            quantity=-10,  # Invalid: negative quantity
            unit_price=Decimal('5.99'),
            reorder_level=20
        )
        item.full_clean()  # Triggers validation

@pytest.mark.django_db
def test_inventory_item_unit_price_validation():
    # Create a Category instance
    category = Category.objects.create(name='Dental Tools', description='Tools used in dental procedures')

    # Test that the 'unit_price' field cannot be negative
    with pytest.raises(ValidationError):
        item = InventoryItem(
            name='Dental Mirror',
            category=category,
            quantity=100,
            unit_price=Decimal('-5.99'),  # Invalid: negative unit_price
            reorder_level=20
        )
        item.full_clean()  # Triggers validation

@pytest.mark.django_db
def test_inventory_item_reorder_level_validation():
    # Create a Category instance
    category = Category.objects.create(name='Dental Tools', description='Tools used in dental procedures')

    # Test that the 'reorder_level' field cannot be negative
    with pytest.raises(ValidationError):
        item = InventoryItem(
            name='Dental Mirror',
            category=category,
            quantity=100,
            unit_price=Decimal('5.99'),
            reorder_level=-20  # Invalid: negative reorder_level
        )
        item.full_clean()  # Triggers validation