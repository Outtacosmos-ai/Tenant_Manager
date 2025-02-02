# tests/test_inventory_apps.py
from django.apps import apps
from apps.inventory.apps import InventoryConfig

def test_inventory_config():
    # Get the app config for the 'inventory' app
    app_config = apps.get_app_config('inventory')
    
    # Assert that the app config is an instance of InventoryConfig
    assert isinstance(app_config, InventoryConfig)
    
    # Assert the default_auto_field is set correctly
    assert app_config.default_auto_field == 'django.db.models.BigAutoField'
    
    # Assert the name of the app is correct
    assert app_config.name == 'apps.inventory'# tests/test_inventory_apps.py
from django.apps import apps
from apps.inventory.apps import InventoryConfig

def test_inventory_config():
    # Get the app config for the 'inventory' app
    app_config = apps.get_app_config('inventory')
    
    # Assert that the app config is an instance of InventoryConfig
    assert isinstance(app_config, InventoryConfig)
    
    # Assert the default_auto_field is set correctly
    assert app_config.default_auto_field == 'django.db.models.BigAutoField'
    
    # Assert the name of the app is correct
    assert app_config.name == 'apps.inventory'