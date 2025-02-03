# tests/test_medical_record_admin.py
import pytest
from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.test import RequestFactory
from apps.inventory.models import MedicalRecord
from apps.inventory.admin import MedicalRecordAdmin

User = get_user_model()

@pytest.fixture
def admin_site():
    return AdminSite()

@pytest.fixture
def medical_record_admin(admin_site):
    return MedicalRecordAdmin(MedicalRecord, admin_site)

@pytest.fixture
def patient():
    return User.objects.create_user(username='patient1', password='testpass123')

@pytest.fixture
def dentist():
    return User.objects.create_user(username='dentist1', password='testpass123')

@pytest.fixture
def medical_record(patient, dentist):
    return MedicalRecord.objects.create(
        patient=patient,
        dentist=dentist,
        diagnosis='Cavity'
    )

@pytest.mark.django_db
def test_medical_record_admin_list_display(medical_record_admin, medical_record):
    # Test the `list_display` attribute
    assert medical_record_admin.list_display == ('patient', 'dentist', 'diagnosis')

    # Test that the `list_display` fields are rendered correctly
    list_display = medical_record_admin.get_list_display(None)
    assert 'patient' in list_display
    assert 'dentist' in list_display
    assert 'diagnosis' in list_display

@pytest.mark.django_db
def test_medical_record_admin_list_filter(medical_record_admin):
    # Test the `list_filter` attribute
    assert medical_record_admin.list_filter == ('dentist',)

@pytest.mark.django_db
def test_medical_record_admin_search_fields(medical_record_admin):
    # Test the `search_fields` attribute
    assert medical_record_admin.search_fields == (
        'patient__user__username', 'dentist__user__username', 'diagnosis'
    )

@pytest.mark.django_db
def test_medical_record_admin_ordering(medical_record_admin):
    # Test the `ordering` attribute
    assert medical_record_admin.ordering == ('-id',)

@pytest.mark.django_db
def test_medical_record_admin_changelist_view(medical_record_admin, medical_record, rf):
    # Create a request object
    request = rf.get('/admin/inventory/medicalrecord/')
    request.user = User.objects.create_superuser(username='admin', password='testpass123')

    # Test the changelist view
    response = medical_record_admin.changelist_view(request)
    assert response.status_code == 200

@pytest.mark.django_db
def test_medical_record_admin_search(medical_record_admin, medical_record, rf):
    # Create a request object with a search query
    request = rf.get('/admin/inventory/medicalrecord/', {'q': 'cavity'})
    request.user = User.objects.create_superuser(username='admin', password='testpass123')

    # Test the search functionality
    response = medical_record_admin.changelist_view(request)
    assert response.status_code == 200
    assert 'cavity' in str(response.content)