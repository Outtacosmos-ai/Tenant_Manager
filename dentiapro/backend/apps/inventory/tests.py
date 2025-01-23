from django.test import TestCase
from .models import InventoryItem, Category
from decimal import Decimal

class InventoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Dental Tools', description='Tools used in dental procedures')
        self.item = InventoryItem.objects.create(
            name='Dental Mirror',
            category=self.category,
            quantity=100,
            unit_price=Decimal('5.99'),
            reorder_level=20
        )

    def test_inventory_item_creation(self):
        self.assertTrue(isinstance(self.item, InventoryItem))
        self.assertEqual(self.item.__str__(), 'Dental Mirror')
        self.assertEqual(self.item.category, self.category)