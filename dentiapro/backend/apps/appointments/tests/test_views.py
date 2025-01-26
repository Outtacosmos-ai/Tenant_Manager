import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

@pytest.mark.django_db
class TestAppointmentsViews:
    def test_index_view(self):
        client = APIClient()
        url = reverse('index')
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {'message': 'Hello, world!'}

    def test_user_viewset(self):
        client = APIClient()
        url = reverse('user-list')
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_group_viewset(self):
        client = APIClient()
        url = reverse('group-list')
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
