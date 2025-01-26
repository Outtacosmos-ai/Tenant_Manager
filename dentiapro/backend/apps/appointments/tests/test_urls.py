import pytest
from django.urls import reverse, resolve
from appointments.views import AppointmentListView, AppointmentDetailView

@pytest.mark.django_db
def test_appointment_list_url():
    url = reverse('appointment-list')
    assert resolve(url).func.view_class == AppointmentListView

@pytest.mark.django_db
def test_appointment_detail_url():
    appointment_id = 1  # Replace with a valid appointment ID
    url = reverse('appointment-detail', args=[appointment_id])
    assert resolve(url).func.view_class == AppointmentDetailView
