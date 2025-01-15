from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from apps.tenants.models import Tenant
from apps.cabinet.models import Cabinet
from apps.appointments.models import Appointment
from apps.medical_records.models import MedicalRecord
from apps.billing.models import Invoice
from apps.inventory.models import InventoryItem

class APITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Creating a tenant for testing
        self.tenant = Tenant.objects.create(name="Test Tenant")

        # Creating related objects for the tenant
        self.cabinet = Cabinet.objects.create(name="Test Cabinet", tenant=self.tenant)
        self.appointment = Appointment.objects.create(
            patient_name="John Doe",
            cabinet=self.cabinet,
            date="2025-01-14",
            status="Scheduled"
        )
        self.medical_record = MedicalRecord.objects.create(
            patient_name="John Doe",
            record_type="General Checkup",
            tenant=self.tenant
        )
        self.invoice = Invoice.objects.create(
            patient_name="John Doe",
            amount=100.00,
            status="Paid",
            tenant=self.tenant
        )
        self.inventory_item = InventoryItem.objects.create(
            name="Test Item",
            quantity=10,
            cabinet=self.cabinet
        )

        # Authenticating the client (assumes authentication is tenant-aware)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer test-token")

    def test_list_cabinets(self):
        """Test retrieving cabinets for a tenant."""
        response = self.client.get('/api/cabinets/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.cabinet.name)

    def test_create_appointment(self):
        """Test creating an appointment."""
        data = {
            "patient_name": "Jane Doe",
            "cabinet": self.cabinet.id,
            "date": "2025-01-15",
            "status": "Scheduled"
        }
        response = self.client.post('/api/appointments/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['patient_name'], "Jane Doe")

    def test_invalid_tenant_access(self):
        """Test access denial when tenant is invalid."""
        self.client.credentials(HTTP_AUTHORIZATION="Bearer invalid-token")
        response = self.client.get('/api/cabinets/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
