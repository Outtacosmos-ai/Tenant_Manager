from django.test import TestCase
from apps.billing.models import Invoice
from apps.patient.models import Patient
from apps.core.models import User
from decimal import Decimal

class BillingTestCase(TestCase):
    def setUp(self):
        # Create a patient
        patient_user = User.objects.create_user(username='patient', password='testpass123')
        self.patient = Patient.objects.create(user=patient_user, date_of_birth='1990-01-01')

        # Create an invoice
        self.invoice = Invoice.objects.create(
            patient=self.patient,
            amount=Decimal('100.00')
        )

    def test_invoice_creation(self):
        self.assertEqual(self.invoice.patient, self.patient)
        self.assertEqual(self.invoice.amount, Decimal('100.00'))
        self.assertFalse(self.invoice.paid)

    def test_invoice_str_representation(self):
        expected_str = f"Invoice {self.invoice.id} - {self.patient}"
        self.assertEqual(str(self.invoice), expected_str)

    def test_invoice_payment(self):
        self.invoice.paid = True
        self.invoice.payment_method = 'Credit Card'
        self.invoice.save()
        self.assertTrue(self.invoice.paid)
        self.assertEqual(self.invoice.payment_method, 'Credit Card')
