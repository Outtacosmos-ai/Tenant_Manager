from django.test import TestCase
from .models import User, Role

class UserModelTest(TestCase):
    def setUp(self):
        self.role = Role.objects.create(name='Doctor', description='Medical professional')
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            role=self.role
        )

    def test_user_creation(self):
        self.assertTrue(isinstance(self.user, User))
        self.assertEqual(self.user.__str__(), 'testuser')
        self.assertEqual(self.user.role, self.role)

class RoleModelTest(TestCase):
    def setUp(self):
        self.role = Role.objects.create(name='Nurse', description='Nursing staff')

    def test_role_creation(self):
        self.assertTrue(isinstance(self.role, Role))
        self.assertEqual(self.role.__str__(), 'Nurse')
