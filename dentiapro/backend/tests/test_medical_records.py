from django.test import TestCase
from apps.medical_records.models import MedicalRecord
from apps.tenant.models import Tenant
from apps.users.models import User
from django.utils import timezone


class MedicalRecordTestCase(TestCase):
    def setUp(self):
        # Create tenant
        self.tenant = Tenant.objects.create(name="Tenant 1")

        # Create users
        self.patient = User.objects.create_user(username='patient', password='testpass123')
        self.dentist = User.objects.create_user(username='dentist', password='testpass123')

        # Create a medical record
        self.medical_record = MedicalRecord.objects.create(
            tenant=self.tenant,
            patient=self.patient,
            dentist=self.dentist,
            diagnosis='Cavity',
            treatment_plan='Filling cavity',
            notes='Patient has anxiety.'
        )

    def test_medical_record_creation(self):
        self.assertEqual(self.medical_record.diagnosis, 'Cavity')
        self.assertEqual(self.medical_record.treatment_plan, 'Filling cavity')
        self.assertEqual(self.medical_record.tenant, self.tenant)

    def test_medical_record_update(self):
        self.medical_record.notes = 'Updated notes: No complications.'
        self.medical_record.save()
        self.assertEqual(self.medical_record.notes, 'Updated notes: No complications.')

    def test_invalid_attachment_format(self):
        with self.assertRaises(ValueError):
            self.medical_record.attachments = 'image.jpg'
            self.medical_record.save()
