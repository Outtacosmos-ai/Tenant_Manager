from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import InventoryItem, Category
from apps.tenant.models import Tenant
from decimal import Decimal

class InventoryModelTest(TestCase):
    def setUp(self):
        self.tenant = Tenant.objects.create(name="Test Tenant")
        self.category = Category.objects.create(
            tenant=self.tenant,
            name="Dental Tools",
            description="Tools used in dental procedures"
        )
        self.item = InventoryItem.objects.create(
            tenant=self.tenant,
            name="Dental Mirror",
            description="A mirror used in dental exams",
            category=self.category,
            quantity=100,
            unit="pcs",
            minimum_quantity=20,
            cost_price=Decimal("5.99")
        )

    def test_inventory_item_creation(self):
        self.assertIsInstance(self.item, InventoryItem)
        self.assertEqual(str(self.item), "Dental Mirror (100 pcs)")
        self.assertEqual(self.item.category, self.category)

    def test_category_creation(self):
        self.assertIsInstance(self.category, Category)
        self.assertEqual(str(self.category), "Dental Tools")

    def test_negative_quantity(self):
        with self.assertRaises(ValueError):
            InventoryItem.objects.create(
                tenant=self.tenant,
                name="Invalid Item",
                description="Should fail due to negative quantity",
                category=self.category,
                quantity=-1,
                unit="pcs",
                minimum_quantity=10,
                cost_price=Decimal("10.00")
            )

class InventoryAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.tenant = Tenant.objects.create(name="Test Tenant")
        self.category = Category.objects.create(
            tenant=self.tenant,
            name="Dental Tools",
            description="Tools used in dental procedures"
        )
        self.item = InventoryItem.objects.create(
            tenant=self.tenant,
            name="Dental Mirror",
            description="A mirror used in dental exams",
            category=self.category,
            quantity=100,
            unit="pcs",
            minimum_quantity=20,
            cost_price=Decimal("5.99")
        )
        self.client.force_authenticate(user=self.tenant.user)  # Assuming a user-tenant relationship

    def test_get_inventory_items(self):
        url = reverse('inventory-item-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.item.name)

    def test_create_inventory_item(self):
        url = reverse('inventory-item-list')
        data = {
            "name": "New Item",
            "description": "A new inventory item",
            "category_id": self.category.id,
            "quantity": 50,
            "unit": "pcs",
            "minimum_quantity": 10,
            "cost_price": "9.99"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(InventoryItem.objects.count(), 2)

    def test_create_inventory_item_negative_quantity(self):
        url = reverse('inventory-item-list')
        data = {
            "name": "Invalid Item",
            "description": "Should fail due to negative quantity",
            "category_id": self.category.id,
            "quantity": -10,
            "unit": "pcs",
            "minimum_quantity": 10,
            "cost_price": "9.99"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("quantity", response.data)

    def test_update_inventory_item(self):
        url = reverse('inventory-item-detail', args=[self.item.id])
        data = {
            "quantity": 150
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.item.refresh_from_db()
        self.assertEqual(self.item.quantity, 150)

    def test_delete_inventory_item(self):
        url = reverse('inventory-item-detail', args=[self.item.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(InventoryItem.objects.count(), 0)

    def test_get_categories(self):
        url = reverse('category-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.category.name)

    def test_create_category(self):
        url = reverse('category-list')
        data = {
            "name": "New Category",
            "description": "A new category description"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)
