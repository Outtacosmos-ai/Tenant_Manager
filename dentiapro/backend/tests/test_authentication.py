from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from apps.users.models import User
from apps.tenant.models import Tenant
from rest_framework.test import APIClient
from django.utils import timezone


class AuthenticationTestCase(TestCase):
    def setUp(self):
        # Set up a tenant instance
        self.tenant = Tenant.objects.create(name="TestTenant")

        # Create users with different roles for authentication tests
        self.patient_user = User.objects.create_user(
            username="patient", password="testpass123", role="patient", tenant=self.tenant
        )
        self.dentist_user = User.objects.create_user(
            username="dentist", password="testpass123", role="dentist", tenant=self.tenant
        )
        self.admin_user = User.objects.create_user(
            username="admin", password="testpass123", role="admin", tenant=self.tenant
        )

        # Create an API client for making requests
        self.client = APIClient()

    def test_user_registration(self):
        """Test user registration."""
        url = reverse("auth:register")  # Make sure this matches your actual URL name
        data = {
            "username": "newuser",
            "password": "newpass123",
            "role": "patient",
            "tenant": self.tenant.id,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 4)
        self.assertEqual(User.objects.get(username="newuser").role, "patient")

    def test_user_login(self):
        """Test user login."""
        url = reverse("auth:login")  # Make sure this matches your actual URL name
        data = {"username": "patient", "password": "testpass123"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", response.data)  # Ensure the response contains an access token

    def test_login_with_invalid_credentials(self):
        """Test login with invalid credentials."""
        url = reverse("auth:login")
        data = {"username": "patient", "password": "wrongpass123"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_role_based_permissions(self):
        """Test role-based permissions for accessing protected endpoints."""
        # Login as patient
        self.client.login(username="patient", password="testpass123")
        response = self.client.get(reverse("appointments-list"))  # Protected endpoint
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("patient", str(response.data))  # Ensure patient is in the response

        # Login as dentist
        self.client.login(username="dentist", password="testpass123")
        response = self.client.get(reverse("appointments-list"))  # Protected endpoint
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("dentist", str(response.data))  # Ensure dentist is in the response

    def test_multitenancy_enforcement(self):
        """Test that users can only access their own tenant data."""
        # Create a second tenant and a user within it
        second_tenant = Tenant.objects.create(name="SecondTenant")
        second_patient = User.objects.create_user(
            username="secondpatient", password="testpass123", role="patient", tenant=second_tenant
        )

        # Login as the first patient
        self.client.login(username="patient", password="testpass123")
        response = self.client.get(reverse("appointments-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn("secondpatient", str(response.data))  # Should not see the second patient’s data

        # Login as the second patient
        self.client.login(username="secondpatient", password="testpass123")
        response = self.client.get(reverse("appointments-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn("patient", str(response.data))  # Should not see the first patient’s data

    def test_access_appointments_without_login(self):
        """Test that non-authenticated users cannot access protected endpoints."""
        url = reverse("appointments-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_password_reset(self):
        """Test password reset functionality (optional)."""
        url = reverse("auth:password_reset")  # Make sure this matches your actual URL name
        data = {"email": self.patient_user.email}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("email", response.data)  # Make sure the email was processed for password reset

    def test_access_appointments_as_admin(self):
        """Test that admin can access all data."""
        self.client.login(username="admin", password="testpass123")
        response = self.client.get(reverse("appointments-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_logout(self):
        """Test user logout functionality."""
        self.client.login(username="patient", password="testpass123")
        url = reverse("auth:logout")  # Make sure this matches your actual URL name
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.logout()
        response = self.client.get(reverse("appointments-list"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  # Should require re-login

