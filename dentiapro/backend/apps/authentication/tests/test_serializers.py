import pytest
from django.contrib.auth.models import Group, User
from rest_framework import serializers
from tutorial.quickstart.serializers import UserSerializer, GroupSerializer


@pytest.fixture
def user_data():
    return {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'groups': []
    }


@pytest.fixture
def group_data():
    return {
        'name': 'testgroup'
    }


@pytest.fixture
def user_serializer():
    return UserSerializer()


@pytest.fixture
def group_serializer():
    return GroupSerializer()


def test_user_serializer(user_data, user_serializer):
    serialized_data = user_serializer.create(user_data)
    assert serialized_data['username'] == user_data['username']
    assert serialized_data['email'] == user_data['email']
    assert serialized_data['groups'] == user_data['groups']


def test_group_serializer(group_data, group_serializer):
    serialized_data = group_serializer.create(group_data)
    assert serialized_data['name'] == group_data['name']
