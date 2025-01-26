import pytest
from django.contrib.auth.models import Group, User
from rest_framework.test import APIRequestFactory, force_authenticate
from tutorial.quickstart.views import UserViewSet, GroupViewSet

@pytest.fixture
def api_factory():
    return APIRequestFactory()

@pytest.fixture
def user():
    return User.objects.create_user(username='testuser', password='testpassword')

@pytest.fixture
def group():
    return Group.objects.create(name='testgroup')

@pytest.mark.django_db
def test_user_view_set_list(api_factory, user):
    view = UserViewSet.as_view({'get': 'list'})
    request = api_factory.get('/api/users/')
    force_authenticate(request, user=user)
    response = view(request)
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['username'] == 'testuser'

@pytest.mark.django_db
def test_group_view_set_list(api_factory, user, group):
    view = GroupViewSet.as_view({'get': 'list'})
    request = api_factory.get('/api/groups/')
    force_authenticate(request, user=user)
    response = view(request)
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['name'] == 'testgroup'
