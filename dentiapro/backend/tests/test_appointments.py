from django.test import TestCase
from apps.appointments.models import Appointment
from apps.patient.models import Patient
from apps.dentist.models import Dentist
from apps.core.models import User
from django.utils import timezone

class AppointmentTestCase(TestCase):
    def setUp(self):
        # Create a patient
        patient_user = User.objects.create_user(username='patient', password='testpass123')
        self.patient = Patient.objects.create(user=patient_user, date_of_birth='1990-01-01')

        # Create a dentist
        dentist_user = User.objects.create_user(username='dentist', password='testpass123')
        self.dentist = Dentist.objects.create(user=dentist_user, specialization='General', license_number='12345')

        # Create an appointment
        self.appointment = Appointment.objects.create(
            patient=self.patient,
            dentist=self.dentist,
            date_time=timezone.now(),
            reason='Checkup'
        )

    def test_appointment_creation(self):
        self.assertEqual(self.appointment.patient, self.patient)
        self.assertEqual(self.appointment.dentist, self.dentist)
        self.assertEqual(self.appointment.reason, 'Checkup')
        self.assertEqual(self.appointment.status, 'SCHEDULED')

    def test_appointment_str_representation(self):
        expected_str = f"{self.patient} - {self.appointment.date_time}"
        self.assertEqual(str(self.appointment), expected_str)

    def test_appointment_status_update(self):
        self.appointment.status = 'CONFIRMED'
        self.appointment.save()
        self.assertEqual(self.appointment.status, 'CONFIRMED')
