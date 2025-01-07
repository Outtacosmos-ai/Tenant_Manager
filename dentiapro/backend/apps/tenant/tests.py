from django.test import TestCase
from .models import Tenant, Domain
from django.utils import timezone

class TenantModelTest(TestCase):
    def setUp(self):
        self.tenant = Tenant.objects.create(
            name='Test Tenant',
            schema_name='test_tenant',
            paid_until=timezone.now().date() + timezone.timedelta(days=30),
            on_trial=True
        )
        self.domain = Domain.objects.create(
            domain='test.example.com',
            tenant=self.tenant,
            is_primary=True
        )

    def test_tenant_creation(self):
        self.assertTrue(isinstance(self.tenant, Tenant))
        self.assertEqual(self.tenant._str_(), 'Test Tenant')

    def test_domain_creation(self):
        self.assertTrue(isinstance(self.domain, Domain))
        self.assertEqual(self.domain.domain, 'test.example.com')