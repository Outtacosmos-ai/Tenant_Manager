from django.test import TestCase
from .models import Patient
from apps.core.models import User

class PatientModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='patient', password='testpass123')
        self.patient = Patient.objects.create(
            user=self.user,
            date_of_birth='1990-01-01',
            address='123 Test St',
            phone='123-456-7890',
            emergency_contact='Jane Doe'
        )

    def test_patient_creation(self):
        
        self.assertTrue(isinstance(self.patient, Patient))
        self.assertEqual(self.patient.__str__(), self.user.get_full_name())