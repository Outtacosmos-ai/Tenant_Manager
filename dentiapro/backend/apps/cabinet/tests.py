from django.test import TestCase
from apps.tenant.models import Tenant
from .models import Cabinet

class CabinetModelTest(TestCase):
    def setUp(self):
        self.tenant = Tenant.objects.create(name="Test Tenant", domain_url="test.com")
        self.cabinet = Cabinet.objects.create(
            tenant=self.tenant,
            name='Test Cabinet',
            address='123 Test St',
            contact_number='1234567890',
            email='test@cabinet.com',
            is_active=True
        )

    def test_cabinet_creation(self):
        self.assertTrue(isinstance(self.cabinet, Cabinet))
        self.assertEqual(str(self.cabinet), 'Test Cabinet')
        self.assertTrue(self.cabinet.is_active)

    def test_cabinet_email_validation(self):
        self.cabinet.email = "invalidemail"
        with self.assertRaises(ValueError):
            self.cabinet.full_clean()

    def test_contact_number_validation(self):
        self.cabinet.contact_number = "123"
        with self.assertRaises(ValueError):
            self.cabinet.full_clean()