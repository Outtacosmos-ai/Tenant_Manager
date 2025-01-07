from django.test import TestCase
from .models import MedicalRecord
from apps.patient.models import Patient
from apps.dentist.models import Dentist
from apps.core.models import User
from django.utils import timezone

class MedicalRecordModelTest(TestCase):
    def setUp(self):
        self.patient_user = User.objects.create_user(username='patient', password='testpass123')
        self.patient = Patient.objects.create(user=self.patient_user, date_of_birth='1990-01-01')
        self.dentist_user = User.objects.create_user(username='dentist', password='testpass123')
        self.dentist = Dentist.objects.create(user=self.dentist_user, license_number='DEN12345')
        self.medical_record = MedicalRecord.objects.create(
            patient=self.patient,
            dentist=self.dentist,
            date=timezone.now().date(),
            diagnosis='Cavity',
            treatment='Filling'
        )

    def test_medical_record_creation(self):
        self.assertTrue(isinstance(self.medical_record, MedicalRecord))
        self.assertEqual(self.medical_record._str_(), f"Medical Record for {self.patient} - {self.medical_record.date}")