from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Patient
from apps.authentication.models import User

class PatientTestCase(TestCase):
    def setUp(self):
        # Create a user and a patient
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client = APIClient()
        self.client.login(username='testuser', password='testpass123')

        self.patient_data = {
            'date_of_birth': '1990-01-01',
            'address': '123 Test Street',
            'phone_number': '1234567890',
            'emergency_contact': 'John Doe'
        }

    def test_create_patient(self):
        response = self.client.post('/patients/', self.patient_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Patient.objects.count(), 1)
        self.assertEqual(Patient.objects.first().address, self.patient_data['address'])

    def test_get_patient(self):
        # Create patient directly
        Patient.objects.create(user=self.user, **self.patient_data)
        response = self.client.get('/patients/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['address'], self.patient_data['address'])

    def test_phone_number_validation(self):
        invalid_data = self.patient_data.copy()
        invalid_data['phone_number'] = 'invalid_phone'
        response = self.client.post('/patients/', invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('phone_number', response.data)

    def test_emergency_contact_validation(self):
        invalid_data = self.patient_data.copy()
        invalid_data['emergency_contact'] = ''
        response = self.client.post('/patients/', invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('emergency_contact', response.data)

    def test_duplicate_patient_creation(self):
        Patient.objects.create(user=self.user, **self.patient_data)
        response = self.client.post('/patients/', self.patient_data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
