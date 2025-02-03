# tests/test_medical_records_apps.py
from django.apps import apps
from apps.medical_records.apps import MedicalRecordsConfig

def test_medical_records_config():
    # Get the app config for the 'medical_records' app
    app_config = apps.get_app_config('medical_records')
    
    # Assert that the app config is an instance of MedicalRecordsConfig
    assert isinstance(app_config, MedicalRecordsConfig)
    
    # Assert the default_auto_field is set correctly
    assert app_config.default_auto_field == 'django.db.models.BigAutoField'
    
    # Assert the name of the app is correct
    assert app_config.name == 'apps.medical_records'