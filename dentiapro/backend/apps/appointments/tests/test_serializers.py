import pytest
from django.contrib.auth.models import User, Group
from rest_framework import serializers
from appointments.serializers import AppointmentSerializer


@pytest.fixture
def user():
    return User.objects.create(username='testuser', email='test@example.com')


@pytest.fixture
def group():
    return Group.objects.create(name='testgroup')


@pytest.fixture
def appointment_data(user, group):
    return {
        'title': 'Test Appointment',
        'description': 'This is a test appointment',
        'date': '2022-01-01',
        'time': '10:00',
        'user': user,
        'group': group,
    }


def test_appointment_serializer(appointment_data):
    serializer = AppointmentSerializer(data=appointment_data)
    assert serializer.is_valid()


def test_appointment_serializer_invalid_data(appointment_data):
    appointment_data['date'] = 'invalid-date'
    serializer = AppointmentSerializer(data=appointment_data)
    assert not serializer.is_valid()
    assert 'date' in serializer.errors


def test_appointment_serializer_save(appointment_data):
    serializer = AppointmentSerializer(data=appointment_data)
    assert serializer.is_valid()
    appointment = serializer.save()
    assert appointment.title == appointment_data['title']
    assert appointment.description == appointment_data['description']
    assert appointment.date == appointment_data['date']
    assert appointment.time == appointment_data['time']
    assert appointment.user == appointment_data['user']
    assert appointment.group == appointment_data['group']
