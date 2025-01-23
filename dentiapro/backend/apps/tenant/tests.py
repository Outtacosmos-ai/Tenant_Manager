from django.test import TestCase
from .models import Tenant, Domain
from django.utils import timezone
from django.db import IntegrityError

class TenantModelTest(TestCase):
    def setUp(self):
        self.tenant = Tenant.objects.create(
            name='Test Tenant',
            schema_name='test_tenant',
            paid_until=timezone.now().date() + timezone.timedelta(days=30),
            on_trial=True,
            email='test@tenant.com'  # Ensure the email is unique
        )
        self.domain = Domain.objects.create(
            domain='test.example.com',
            tenant=self.tenant,
            is_primary=True
        )

    def test_tenant_creation(self):
        self.assertTrue(isinstance(self.tenant, Tenant))
        self.assertEqual(str(self.tenant), 'Test Tenant')

    def test_domain_creation(self):
        self.assertTrue(isinstance(self.domain, Domain))
        self.assertEqual(self.domain.domain, 'test.example.com')

    def test_tenant_email_uniqueness(self):
        with self.assertRaises(IntegrityError):
            Tenant.objects.create(
                name='Duplicate Tenant',
                schema_name='duplicate_tenant',
                email=self.tenant.email  # This should raise an error
            )