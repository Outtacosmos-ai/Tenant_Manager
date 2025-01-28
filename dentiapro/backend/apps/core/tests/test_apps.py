import pytest
from django.apps import apps
from django.conf import settings
from apps.core.apps import CoreConfig

def test_core_app_config():
    """
    Test the CoreConfig application configuration
    """
    # Get the app config
    app_config = apps.get_app_config('core')
    
    # Verify the app config is an instance of CoreConfig
    assert isinstance(app_config, CoreConfig)
    
    # Check the name attribute
    assert app_config.name == 'apps.core'
    
    # Verify the default auto field
    assert app_config.default_auto_field == 'django.db.models.BigAutoField'

def test_core_app_in_installed_apps():
    """
    Ensure the core app is in INSTALLED_APPS
    """
    assert 'apps.core' in settings.INSTALLED_APPS

@pytest.mark.django_db
def test_app_config_ready_method():
    """
    Test the ready() method of the app config
    
    Note: This test is a placeholder and should be customized 
    based on any specific setup in the ready() method
    """
    # Get the app config
    app_config = apps.get_app_config('core')
    
    # If the CoreConfig has a custom ready() method, you might want to:
    # 1. Check if the method exists
    # 2. Verify any side effects of the ready() method
    
    # Example checks (modify based on your actual implementation)
    try:
        # If there's a custom ready() method, call it
        if hasattr(app_config, 'ready'):
            app_config.ready()
    except Exception as e:
        # Fail the test if an unexpected error occurs
        pytest.fail(f"Error in app config ready method: {str(e)}")

def test_app_config_verbose_name():
    """
    Optional: Test the verbose name of the app config
    """
    app_config = apps.get_app_config('core')
    
    # If you've set a verbose_name in the AppConfig
    # assert app_config.verbose_name == 'Expected Verbose Name'
    
    # Alternatively, check that it has a default verbose name
    assert hasattr(app_config, 'verbose_name')

def test_app_config_dependencies():
    """
    Test any dependencies of the core app
    """
    app_config = apps.get_app_config('core')
    
    # If your CoreConfig has any specific dependencies
    # Check that they are installed or configured
    # Example:
    # required_apps = ['django.contrib.auth', 'some_other_app']
    # for app in required_apps:
    #     assert app in settings.INSTALLED_APPS

def test_app_config_path():
    """
    Verify the path of the core app
    """
    app_config = apps.get_app_config('core')
    
    # Check that the app has a valid path
    assert hasattr(app_config, 'path')
    assert app_config.path is not None
    
    # Optionally, check the path exists
    import os
    assert os.path.exists(app_config.path)

@pytest.mark.django_db
def test_app_config_model_registration():
    """
    Test model registration for the core app
    """
    app_config = apps.get_app_config('core')
    
    # Get all models for this app
    models = app_config.get_models()
    
    # If you expect specific models in the core app
    # expected_models = [User, Permission, etc.]
    # assert set(models) == set(expected_models)
    
    # Basic checks
    assert hasattr(app_config, 'get_models')
    
    # Verify that models can be retrieved
    try:
        list(models)
    except Exception as e:
        pytest.fail(f"Error retrieving models: {str(e)}")

# Optional: Fixture for app config if needed in other tests
@pytest.fixture
def core_app_config():
    """
    Fixture to provide the CoreConfig
    """
    return apps.get_app_config('core')