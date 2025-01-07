from django.test import TestCase
from .models import Invoice
from apps.patient.models import Patient
from apps.core.models import User
from decimal import Decimal

class InvoiceModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.patient = Patient.objects.create(user=self.user, date_of_birth='1990-01-01')
        self.invoice = Invoice.objects.create(
            patient=self.patient,
            amount=Decimal('100.00')
        )

    def test_invoice_creation(self):
        self.assertTrue(isinstance(self.invoice, Invoice))
        self.assertEqual(self.invoice.__str__(), f"Invoice {self.invoice.id} - {self.patient}")
