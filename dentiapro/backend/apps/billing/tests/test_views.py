import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from unittest.mock import Mock, patch

# Assuming these are your actual models and serializers
from apps.billing.models import Invoice, Patient
from apps.billing.serializers import InvoiceSerializer
from apps.billing.views import InvoiceViewSet

@pytest.mark.django_db
class TestInvoiceViewSet:
    def setup_method(self):
        """
        Setup method to initialize test environment
        """
        self.client = APIClient()
        self.view = InvoiceViewSet()

    def create_test_invoices(self, user, num_invoices=5):
        """
        Helper method to create test invoices
        """
        invoices = []
        for i in range(num_invoices):
            invoice = Invoice.objects.create(
                patient=user,
                invoice_number=f'INV-2023-{i}',
                amount=100.00 * (i + 1),
                status='draft'
            )
            invoices.append(invoice)
        return invoices

    def test_get_queryset_patient_role(self, create_patient_user):
        """
        Test queryset filtering for patient role
        """
        # Create a patient user and their invoices
        patient_user = create_patient_user
        self.client.force_authenticate(user=patient_user)

        # Create invoices for the patient and another patient
        patient_invoices = self.create_test_invoices(patient_user)
        another_patient = Patient.objects.create(
            first_name='Another', 
            last_name='Patient', 
            email='another@example.com'
        )
        other_invoices = self.create_test_invoices(another_patient)

        # Simulate request
        request = Mock()
        request.user = patient_user
        request.user.role = 'patient'

        # Set up view with the mock request
        self.view.request = request
        self.view.kwargs = {}

        # Get the queryset
        queryset = self.view.get_queryset()

        # Assert only patient's own invoices are returned
        assert queryset.count() == len(patient_invoices)
        for invoice in queryset:
            assert invoice.patient == patient_user

    def test_get_queryset_non_patient_role(self, create_admin_user):
        """
        Test queryset for non-patient roles (e.g., admin, dentist)
        """
        # Create an admin user
        admin_user = create_admin_user
        self.client.force_authenticate(user=admin_user)

        # Create invoices for multiple patients
        patients = []
        all_invoices = []
        for i in range(3):
            patient = Patient.objects.create(
                first_name=f'Patient{i}', 
                last_name='Test', 
                email=f'patient{i}@example.com'
            )
            patients.append(patient)
            all_invoices.extend(self.create_test_invoices(patient))

        # Simulate request
        request = Mock()
        request.user = admin_user
        request.user.role = 'admin'  # or 'dentist'

        # Set up view with the mock request
        self.view.request = request
        self.view.kwargs = {}

        # Get the queryset
        queryset = self.view.get_queryset()

        # Assert all invoices are returned
        assert queryset.count() == len(all_invoices)

    def test_invoice_list_view(self, create_patient_user):
        """
        Test invoice list view endpoint
        """
        # Create a patient user and their invoices
        patient_user = create_patient_user
        self.client.force_authenticate(user=patient_user)

        # Create invoices for the patient
        self.create_test_invoices(patient_user)

        # Get the list endpoint
        url = reverse('invoice-list')  # Adjust based on your URL configuration
        response = self.client.get(url)

        # Assert response
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 5  # Number of created invoices

    def test_invoice_create_view(self, create_patient_user):
        """
        Test invoice creation endpoint
        """
        # Create a patient user
        patient_user = create_patient_user
        self.client.force_authenticate(user=patient_user)

        # Prepare invoice data
        invoice_data = {
            'patient': patient_user.id,
            'invoice_number': 'INV-2023-NEW',
            'amount': 250.00,
            'status': 'draft'
        }

        # Get the create endpoint
        url = reverse('invoice-list')  # Adjust based on your URL configuration
        response = self.client.post(url, invoice_data)

        # Assert response
        assert response.status_code == status.HTTP_201_CREATED
        assert Invoice.objects.filter(invoice_number='INV-2023-NEW').exists()

    def test_invoice_unauthorized_access(self):
        """
        Test unauthorized access to invoice endpoints
        """
        # Create URLs for different actions
        list_url = reverse('invoice-list')
        detail_url = reverse('invoice-detail', kwargs={'pk': 1})

        # Test list view
        response = self.client.get(list_url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        # Test detail view
        response = self.client.get(detail_url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

# Fixtures for creating test users
@pytest.fixture
def create_patient_user(django_user_model):
    """
    Fixture to create a patient user
    """
    user = django_user_model.objects.create_user(
        username='patient',
        email='patient@example.com',
        password='testpass123',
        role='patient'
    )
    return user

@pytest.fixture
def create_admin_user(django_user_model):
    """
    Fixture to create an admin user
    """
    user = django_user_model.objects.create_user(
        username='admin',
        email='admin@example.com',
        password='testpass123',
        role='admin'
    )
    return user