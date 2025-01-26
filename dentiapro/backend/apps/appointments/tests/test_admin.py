from django.contrib.admin.sites import AdminSite
from django.test import TestCase, RequestFactory

from appointments.admin import AppointmentAdmin
from appointments.models import Appointment

class AppointmentAdminTest(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.factory = RequestFactory()

    def test_appointment_admin_should_display_correct_fields(self):
        appointment_admin = AppointmentAdmin(Appointment, self.site)
        appointment = Appointment.objects.create(
            title='Test Appointment',
            description='This is a test appointment',
            date='2022-01-01',
            time='10:00',
        )

        request = self.factory.get('/admin/appointments/appointment/')
        response = appointment_admin.change_view(request, str(appointment.id))

        self.assertContains(response, 'Test Appointment')
        self.assertContains(response, 'This is a test appointment')
        self.assertContains(response, '2022-01-01')
        self.assertContains(response, '10:00')

    def test_appointment_admin_should_be_able_to_change_fields(self):
        appointment_admin = AppointmentAdmin(Appointment, self.site)
        appointment = Appointment.objects.create(
            title='Test Appointment',
            description='This is a test appointment',
            date='2022-01-01',
            time='10:00',
        )

        request = self.factory.post(
            '/admin/appointments/appointment/',
            {
                'title': 'Updated Appointment',
                'description': 'This is an updated appointment',
                'date': '2022-01-02',
                'time': '11:00',
            },
        )
        request.user = self.client.user
        response = appointment_admin.change_view(request, str(appointment.id))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(appointment.title, 'Updated Appointment')
        self.assertEqual(appointment.description, 'This is an updated appointment')
        self.assertEqual(appointment.date, '2022-01-02')
        self.assertEqual(appointment.time, '11:00')
