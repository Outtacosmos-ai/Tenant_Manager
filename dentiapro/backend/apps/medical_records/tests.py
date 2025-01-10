from django.test import TestCase
from .models import MedicalRecord
from apps.tenant.models import Tenant
from apps.users.models import User
from django.utils import timezone


class MedicalRecordModelTest(TestCase):
    def setUp(self):
        # Create tenant
        self.tenant = Tenant.objects.create(name="Tenant 1")

        # Create users
        self.patient = User.objects.create_user(username='patient', password='testpass123')
        self.dentist = User.objects.create_user(username='dentist', password='testpass123')

        # Create medical record
        self.medical_record = MedicalRecord.objects.create(
            tenant=self.tenant,
            patient=self.patient,
            dentist=self.dentist,
            diagnosis='Tooth decay',
            treatment_plan='Fill cavity',
            notes='Patient is sensitive to anesthesia.'
        )

    def test_medical_record_creation(self):
        self.assertEqual(self.medical_record.diagnosis, 'Tooth decay')
        self.assertEqual(self.medical_record.treatment_plan, 'Fill cavity')
        self.assertEqual(self.medical_record.tenant, self.tenant)

    def test_medical_record_str_representation(self):
        self.assertEqual(
            str(self.medical_record),
            f"Medical Record for {self.patient} - {self.medical_record.created_at.date()}"
        )
