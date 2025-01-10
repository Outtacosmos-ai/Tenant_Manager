from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from apps.appointments.models import Appointment
from apps.users.models import User
from apps.cabinet.models import Cabinet
from apps.tenant.models import Tenant

class AppointmentAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        # Set up tenant, cabinet, users (dentist and patient)
        self.tenant = Tenant.objects.create(name="Test Tenant", domain_url="test.com")
        self.cabinet = Cabinet.objects.create(tenant=self.tenant, name="Test Cabinet")
        self.dentist = User.objects.create_user(username="dentist", email="dentist@test.com", password="testpass123", role="dentist", tenant=self.tenant)
        self.patient = User.objects.create_user(username="patient", email="patient@test.com", password="testpass123", role="patient", tenant=self.tenant)
        
        # Create an appointment
        self.appointment = Appointment.objects.create(
            patient=self.patient,
            dentist=self.dentist,
            cabinet=self.cabinet,
            date_time="2023-06-01T10:00:00Z",
            duration="01:00:00",
            status="scheduled"
        )
        
        # Authenticate dentist user
        self.client.force_authenticate(user=self.dentist)

    def test_list_appointments(self):
        url = reverse('appointment-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)  # Ensure one appointment is returned

    def test_create_appointment(self):
        url = reverse('appointment-list')
        data = {
            "patient": self.patient.id,
            "dentist": self.dentist.id,
            "cabinet": self.cabinet.id,
            "date_time": "2023-06-02T11:00:00Z",
            "duration": "01:00:00",
            "status": "scheduled"
        }
        response = self.client.post(url, data, format='json')  # Ensure proper content type is set
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Appointment.objects.count(), 2)  # Check if the count is updated correctly

    def test_retrieve_appointment(self):
        url = reverse('appointment-detail', kwargs={'pk': self.appointment.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], str(self.appointment.id))  # Ensure the correct appointment is returned

    def test_update_appointment(self):
        url = reverse('appointment-detail', kwargs={'pk': self.appointment.id})
        data = {
            "status": "completed"
        }
        response = self.client.patch(url, data, format='json')  # Ensure proper content type is set
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.appointment.refresh_from_db()
        self.assertEqual(self.appointment.status, "completed")  # Ensure the status is updated correctly

    def test_delete_appointment(self):
        url = reverse('appointment-detail', kwargs={'pk': self.appointment.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Appointment.objects.count(), 0)  # Ensure appointment is deleted

    def test_appointments_patient_access(self):
        self.client.force_authenticate(user=self.patient)  # Authenticate as a patient
        
        url = reverse('appointment-list')
        response = self.client.get(url)
        
        # Patient should only see their own appointments
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)  # Patient should see their own appointment
        
    def test_appointments_dentist_access(self):
        self.client.force_authenticate(user=self.dentist)  # Authenticate as dentist
        
        url = reverse('appointment-list')
        response = self.client.get(url)
        
        # Dentist should see their own appointments
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)  # Dentist should see the patient appointment

    def test_appointments_permissions(self):
        # Test permission by trying to access appointments as an unauthenticated user
        self.client.force_authenticate(user=None)
        url = reverse('appointment-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  # Should return 401 if not authenticated
