from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from apps.billing.models import Invoice
from apps.users.models import User
from apps.cabinet.models import Cabinet
from apps.tenant.models import Tenant

class BillingTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create a tenant for testing
        self.tenant = Tenant.objects.create(name="Test Tenant", domain_url="test.com")

        # Create a cabinet for the tenant
        self.cabinet = Cabinet.objects.create(tenant=self.tenant, name="Test Cabinet")

        # Create users (dentist and patient) associated with the tenant
        self.dentist = User.objects.create_user(
            username="dentist", email="dentist@test.com", password="testpass123", role="dentist", tenant=self.tenant
        )
        self.patient = User.objects.create_user(
            username="patient", email="patient@test.com", password="testpass123", role="patient", tenant=self.tenant
        )

        # Create an invoice associated with the patient, dentist, and cabinet
        self.invoice = Invoice.objects.create(
            patient=self.patient, dentist=self.dentist, cabinet=self.cabinet, amount=100, status="pending"
        )

        # Authenticate the client with the dentist's credentials
        self.client.force_authenticate(user=self.dentist)

    def test_create_invoice(self):
        """Test that a dentist can create an invoice."""
        url = reverse('invoice-list')
        data = {
            "patient": self.patient.id,
            "dentist": self.dentist.id,
            "cabinet": self.cabinet.id,
            "amount": 200,
            "status": "pending"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Invoice.objects.count(), 2)

    def test_list_invoices(self):
        """Test that a dentist can list all invoices."""
        url = reverse('invoice-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)  # Should only return one invoice

    def test_retrieve_invoice(self):
        """Test that a dentist can retrieve a specific invoice."""
        url = reverse('invoice-detail', kwargs={'pk': self.invoice.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], str(self.invoice.id))  # Check invoice ID

    def test_create_invoice_unauthorized(self):
        """Test that a patient cannot create an invoice."""
        self.client.force_authenticate(user=self.patient)
        url = reverse('invoice-list')
        data = {
            "patient": self.patient.id,
            "dentist": self.dentist.id,
            "cabinet": self.cabinet.id,
            "amount": 200,
            "status": "pending"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Patient should be forbidden

    def test_invoice_amount_and_details(self):
        """Test that the invoice details (amount, patient, dentist) are correct."""
        self.assertEqual(self.invoice.amount, 100)
        self.assertEqual(self.invoice.patient.username, "patient")
        self.assertEqual(self.invoice.dentist.username, "dentist")

    def test_update_invoice_status(self):
        """Test that a dentist can update an invoice status."""
        url = reverse('invoice-detail', kwargs={'pk': self.invoice.id})
        data = {"status": "paid"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.invoice.refresh_from_db()
        self.assertEqual(self.invoice.status, "paid")

    def test_invoice_str_representation(self):
        """Test that the invoice's string representation is correct."""
        expected_str = f"Invoice {self.invoice.id} - {self.patient.username}"
        self.assertEqual(str(self.invoice), expected_str)

    def test_tenant_isolation(self):
        """Test that invoices are tenant-specific and not visible across tenants."""
        second_tenant = Tenant.objects.create(name="Second Tenant", domain_url="second.com")
        second_patient = User.objects.create_user(
            username="secondpatient", email="second@test.com", password="testpass123", role="patient", tenant=second_tenant
        )
        second_invoice = Invoice.objects.create(
            patient=second_patient, dentist=self.dentist, cabinet=self.cabinet, amount=150, status="pending"
        )

        # Attempt to retrieve invoice from a different tenant (should not be visible)
        self.client.force_authenticate(user=self.dentist)
        url = reverse('invoice-detail', kwargs={'pk': second_invoice.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_access_unauthenticated(self):
        """Test that an unauthenticated user cannot access invoices."""
        self.client.force_authenticate(user=None)
        url = reverse('invoice-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
