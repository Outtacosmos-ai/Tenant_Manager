import pytest
from django.contrib.auth.models import Group, User
from rest_framework import serializers
from cabinet.serializers import CabinetSerializer

@pytest.fixture
def user():
    return User.objects.create(username='testuser', email='test@example.com')

@pytest.fixture
def group():
    return Group.objects.create(name='testgroup')

@pytest.fixture
def cabinet_serializer():
    return CabinetSerializer()

def test_user_serializer(user):
    data = {
        'url': 'http://example.com/users/1/',
        'username': 'testuser',
        'email': 'test@example.com',
        'groups': []
    }
    serializer = serializers.UserSerializer(instance=user)
    assert serializer.data == data

def test_group_serializer(group):
    data = {
        'url': 'http://example.com/groups/1/',
        'name': 'testgroup'
    }
    serializer = serializers.GroupSerializer(instance=group)
    assert serializer.data == data

def test_cabinet_serializer(cabinet_serializer):
    data = {
        # Add the expected data for the CabinetSerializer here
    }
    # Create a test case for the CabinetSerializer
    assert cabinet_serializer.data == data
