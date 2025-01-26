import pytest
from django.apps import apps
from tutorial.quickstart.apps import QuickstartConfig


@pytest.mark.django_db
def test_quickstart_config():
    # Check if the QuickstartConfig class exists
    assert apps.is_installed('quickstart')
    assert QuickstartConfig.name == 'quickstart'
    assert QuickstartConfig.default_auto_field == 'django.db.models.BigAutoField'
