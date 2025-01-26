import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from apps.authentication.models import UserProfile

User = get_user_model()

@pytest.mark.django_db
def test_user_profile_creation():
    # Create a user
    user = User.objects.create_user(username='testuser', password='testpassword')
    
    # Create a user profile
    user_profile = UserProfile.objects.create(user=user, bio='Test bio')
    
    # Check if the user profile is created successfully
    assert user_profile.user == user
    assert user_profile.bio == 'Test bio'

@pytest.mark.django_db
def test_user_profile_creation_without_user():
    # Try to create a user profile without a user
    with pytest.raises(ValidationError):
        UserProfile.objects.create(bio='Test bio')

@pytest.mark.django_db
def test_user_profile_str_representation():
    # Create a user
    user = User.objects.create_user(username='testuser', password='testpassword')
    
    # Create a user profile
    user_profile = UserProfile.objects.create(user=user, bio='Test bio')
    
    # Check if the __str__ method returns the expected string representation
    assert str(user_profile) == f"Profile for {user.username}"
