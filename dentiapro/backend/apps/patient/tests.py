from django.test import TestCase
from .models import Patient

class PatientModelTest(TestCase):
    def setUp(self):
        Patient.objects.create(
            first_name="John",
            last_name="Doe",
            date_of_birth="1990-01-01",
            email="john@example.com",
            phone="123-456-7890"
        )

    def test_patient_creation(self):
        patient = Patient.objects.get(email="john@example.com")
        self.assertEqual(patient.first_name, "John")
        self.assertEqual(patient.last_name, "Doe")

