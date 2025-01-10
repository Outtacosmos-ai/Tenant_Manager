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
            tenant=self.patient.tenant,  # Ensure multi-tenancy support
            patient=self.patient,
            dentist=self.dentist,
            date=timezone.now().date() + timezone.timedelta(days=1),
            start_time=timezone.now().time(),
            end_time=timezone.now().time(),
            status='scheduled',
        )

    def test_appointment_creation(self):
        self.assertTrue(isinstance(self.appointment, Appointment))
        self.assertEqual(self.appointment.status, 'scheduled')
        self.assertEqual(str(self.appointment), f"{self.patient} - {self.appointment.date} {self.appointment.start_time}")
