import pytest
from django.apps import apps
from django.conf import settings
from apps.authentication.apps import AuthenticationConfig

def test_authentication_app_config():
    # Check if the app config is correctly registered
    app_config = apps.get_app_config('authentication')
    
    # Verify the app config is an instance of AuthenticationConfig
    assert isinstance(app_config, AuthenticationConfig)
    
    # Check the name attribute
    assert app_config.name == 'apps.authentication'
    
    # Verify the default auto field
    assert app_config.default_auto_field == 'django.db.models.BigAutoField'

def test_authentication_app_in_installed_apps():
    # Ensure the app is in INSTALLED_APPS
    assert 'apps.authentication' in settings.INSTALLED_APPS

@pytest.mark.django_db
def test_app_config_ready_method():
    # If the AuthenticationConfig has a ready() method, you can test it
    # This is an optional test and depends on your specific implementation
    app_config = apps.get_app_config('authentication')
    
    # If you have any specific setup or checks in the ready() method
    # you can add assertions here
    # For example:
    # assert hasattr(app_config, 'some_attribute')
    # or
    # app_config.ready()  # Call the ready method if it exists
    pass
