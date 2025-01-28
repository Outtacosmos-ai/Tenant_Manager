import pytest
from cabinet.models import Cabinet

@pytest.mark.django_db
def test_cabinet_creation():
    # Create a Cabinet object
    cabinet = Cabinet.objects.create(name="Test Cabinet", location="Test Location")

    # Check if the Cabinet object is created successfully
    assert cabinet.name == "Test Cabinet"
    assert cabinet.location == "Test Location"
    assert cabinet.created_at is not None
    assert cabinet.updated_at is not None

    # Check if the Cabinet object can be retrieved from the database
    retrieved_cabinet = Cabinet.objects.get(name="Test Cabinet")
    assert retrieved_cabinet == cabinet

    # Check if the Cabinet object can be updated
    cabinet.name = "Updated Cabinet"
    cabinet.save()
    updated_cabinet = Cabinet.objects.get(name="Updated Cabinet")
    assert updated_cabinet == cabinet

    # Check if the Cabinet object can be deleted
    cabinet.delete()
    with pytest.raises(Cabinet.DoesNotExist):
        Cabinet.objects.get(name="Updated Cabinet")
