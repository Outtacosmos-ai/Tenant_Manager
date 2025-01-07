from django.test import TestCase
from .models import Dentist, Specialization
from apps.core.models import User

class DentistModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='dentist', password='testpass123')
        self.specialization = Specialization.objects.create(name='Orthodontics', description='Teeth alignment')
        self.dentist = Dentist.objects.create(
            user=self.user,
            specialization=self.specialization,
            license_number='DEN12345',
            years_of_experience=5
        )

    def test_dentist_creation(self):
        self.assertTrue(isinstance(self.dentist, Dentist))
        self.assertEqual(self.dentist._str_(), f"Dr. {self.user.get_full_name()}")