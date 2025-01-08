from django.test import TestCase
from apps.medical_records.models import MedicalRecord
from apps.patient.models import Patient
from apps.dentist.models import Dentist
from apps.core.models import User
from django.utils import timezone

class MedicalRecordTestCase(TestCase):
    def setUp(self):
        # Create a patient
        patient_user = User.objects.create_user(username='patient', password='testpass123')
        self.patient = Patient.objects.create(user=patient_user, date_of_birth='1990-01-01')

        # Create a dentist
        dentist_user = User.objects.create_user(username='dentist', password='testpass123')
        self.dentist = Dentist.objects.create(user=dentist_user, specialization='General', license_number='12345')

        # Create a medical record
        self.medical_record = MedicalRecord.objects.create(
            patient=self.patient,
            dentist=self.dentist,
            date=timezone.now().date(),
            diagnosis='Cavity',
            treatment='Filling'
        )

    def test_medical_record_creation(self):
        self.assertEqual(self.medical_record.patient, self.patient)
        self.assertEqual(self.medical_record.dentist, self.dentist)
        self.assertEqual(self.medical_record.diagnosis, 'Cavity')
        self.assertEqual(self.medical_record.treatment, 'Filling')

    def test_medical_record_str_representation(self):
        expected_str = f"Medical Record for {self.patient} - {self.medical_record.date}"
        self.assertEqual(str(self.medical_record), expected_str)

    def test_medical_record_update(self):
        self.medical_record.notes = 'Patient responded well to treatment'
        self.medical_record.save()
        self.assertEqual(self.medical_record.notes, 'Patient responded well to treatment')
