from django.test import TestCase
from .models import Appointment
from apps.patient.models import Patient
from apps.dentist.models import Dentist
from apps.core.models import User
from django.utils import timezone

class AppointmentModelTest(TestCase):
    def setUp(self):
        self.patient_user = User.objects.create_user(username='patient', password='testpass123')
        self.patient = Patient.objects.create(user=self.patient_user, date_of_birth='1990-01-01')
        self.dentist_user = User.objects.create_user(username='dentist', password='testpass123')
        self.dentist = Dentist.objects.create(user=self.dentist_user, specialization='General')
        self.appointment = Appointment.objects.create(
            patient=self.patient,
            dentist=self.dentist,
            date_time=timezone.now(),
            reason='Checkup'
        )

    def test_appointment_creation(self):
        self.assertTrue(isinstance(self.appointment, Appointment))
        self.assertEqual(self.appointment.__str__(), f"{self.patient} - {self.appointment.date_time}")
