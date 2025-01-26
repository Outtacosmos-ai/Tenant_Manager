import pytest
from django.apps import apps
from appointments.apps import AppointmentsConfig


@pytest.mark.django_db
def test_app_config():
    assert AppointmentsConfig.name == 'appointments'
    assert apps.get_app_config('appointments').name == 'appointments'
