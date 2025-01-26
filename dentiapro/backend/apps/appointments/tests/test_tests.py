import pytest
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from appointments.models import Appointment
from appointments.serializers import AppointmentSerializer

@pytest.mark.django_db
class AppointmentTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.appointment_data = {
            'title': 'Test Appointment',
            'date': '2022-01-01',
            'time': '10:00',
            'description': 'This is a test appointment',
        }
        self.response = self.client.post(
            reverse('appointments:create'),
            self.appointment_data,
            format='json'
        )

    def test_create_appointment(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        appointment = Appointment.objects.get()
        self.assertEqual(appointment.title, self.appointment_data['title'])
        self.assertEqual(appointment.date, self.appointment_data['date'])
        self.assertEqual(appointment.time, self.appointment_data['time'])
        self.assertEqual(appointment.description, self.appointment_data['description'])

    def test_get_appointment_list(self):
        response = self.client.get(reverse('appointments:list'))
        appointments = Appointment.objects.all()
        serializer = AppointmentSerializer(appointments, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_appointment(self):
        appointment = Appointment.objects.get()
        response = self.client.get(reverse('appointments:detail', kwargs={'pk': appointment.id}))
        serializer = AppointmentSerializer(appointment)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_appointment(self):
        appointment = Appointment.objects.get()
        updated_data = {
            'title': 'Updated Appointment',
            'date': '2022-01-02',
            'time': '11:00',
            'description': 'This is an updated appointment',
        }
        response = self.client.put(
            reverse('appointments:update', kwargs={'pk': appointment.id}),
            updated_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        appointment.refresh_from_db()
        self.assertEqual(appointment.title, updated_data['title'])
        self.assertEqual(appointment.date, updated_data['date'])
        self.assertEqual(appointment.time, updated_data['time'])
        self.assertEqual(appointment.description, updated_data['description'])

    def test_delete_appointment(self):
        appointment = Appointment.objects.get()
        response = self.client.delete(reverse('appointments:delete', kwargs={'pk': appointment.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Appointment.objects.count(), 0)
