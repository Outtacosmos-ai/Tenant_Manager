from django.test import TestCase
from .models import Cabinet

class CabinetModelTest(TestCase):
    def setUp(self):
        self.cabinet = Cabinet.objects.create(
            name='Test Cabinet',
            address='123 Test St',
            contact_number='123-456-7890',
            email='test@cabinet.com'
        )

    def test_cabinet_creation(self):
        self.assertTrue(isinstance(self.cabinet, Cabinet))
        self.assertEqual(self.cabinet._str_(), 'Test Cabinet')