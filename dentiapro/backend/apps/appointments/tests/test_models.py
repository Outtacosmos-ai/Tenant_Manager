import pytest
from django.contrib.auth.models import User
from _appointments.models import Appointment

@pytest.mark.django_db
def test_appointment_creation():
    # Create a user for testing
    user = User.objects.create(username='testuser')

    # Create an appointment
    appointment = Appointment.objects.create(
        user=user,
        title='Test Appointment',
        description='This is a test appointment',
        start_time='2022-01-01 10:00:00',
        end_time='2022-01-01 11:00:00'
    )

    # Check if the appointment was created successfully
    assert appointment.title == 'Test Appointment'
    assert appointment.description == 'This is a test appointment'
    assert appointment.start_time.strftime('%Y-%m-%d %H:%M:%S') == '2022-01-01 10:00:00'
    assert appointment.end_time.strftime('%Y-%m-%d %H:%M:%S') == '2022-01-01 11:00:00'
    assert appointment.user == user
