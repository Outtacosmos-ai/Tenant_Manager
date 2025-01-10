from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from apps.tenant.models import Tenant
from .models import Cabinet

class CabinetAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.tenant = Tenant.objects.create(name="Test Tenant", domain_url="test.com")
        self.cabinet = Cabinet.objects.create(
            tenant=self.tenant,
            name="Test Cabinet",
            address="123 Test St",
            contact_number="1234567890",
            email="test@cabinet.com",
            is_active=True
        )

    def test_list_cabinets(self):
        response = self.client.get('/api/cabinets/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_create_cabinet(self):
        data = {
            "tenant": self.tenant.id,
            "name": "New Cabinet",
            "address": "456 Test Ave",
            "contact_number": "0987654321",
            "email": "new@cabinet.com",
            "is_active": True
        }
        response = self.client.post('/api/cabinets/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Cabinet.objects.count(), 2)

    def test_update_cabinet(self):
        data = {"name": "Updated Cabinet"}
        response = self.client.patch(f'/api/cabinets/{self.cabinet.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Cabinet.objects.get(id=self.cabinet.id).name, "Updated Cabinet")

    def test_delete_cabinet(self):
        response = self.client.delete(f'/api/cabinets/{self.cabinet.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Cabinet.objects.count(), 0)
