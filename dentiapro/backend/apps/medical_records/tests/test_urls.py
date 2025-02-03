import pytest
from django.urls import reverse, resolve
from medical_records.views import MedicalRecordViewSet

@pytest.mark.parametrize("url_name,viewset_action", [
    ("medicalrecord-list", "list"),
    ("medicalrecord-detail", "retrieve"),
])
@pytest.mark.django_db
def test_medical_record_urls(url_name, viewset_action):
    if url_name == "medicalrecord-detail":
        url = reverse(url_name, kwargs={"pk": 1})  # Example ID
    else:
        url = reverse(url_name)
    
    resolved_func = resolve(url).func.cls
    assert resolved_func == MedicalRecordViewSet
