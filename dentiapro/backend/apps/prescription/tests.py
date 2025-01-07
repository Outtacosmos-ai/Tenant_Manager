from django.test import TestCase
from .models import Prescription
from apps.patient.models import Patient
from apps.dentist.models import Dentist
from apps.core.models import User
from django.utils import timezone

class PrescriptionModelTest(TestCase):
    def setUp(self):
        self.patient_user = User.objects.create_user(username='patient', password='testpass123')
        self.patient = Patient.objects.create(user=self.patient_user, date_of_birth='1990-01-01')
        self.dentist_user = User.objects.create_user(username='dentist', password='testpass123')
        self.dentist = Dentist.objects.create(user=self.dentist_user, license_number='DEN12345')
        self.prescription = Prescription.objects.create(
            patient=self.patient,
            dentist=self.dentist,
            medication='Amoxicillin',
            dosage='500mg',
            frequency='3 times a day',
            duration='7 days'
        )

    def test_prescription_creation(self):
        self.assertTrue(isinstance(self.prescription, Prescription))
        self.assertEqual(self.prescription.__str__(), f"Prescription for {self.patient} - {self.prescription.date}")
