import pytest
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model

# Assuming these are your actual models
from apps.dentist.models import Specialization, Dentist
from apps.users.models import User

@pytest.mark.django_db
class TestSpecializationModel:
    def test_create_specialization(self):
        """
        Test creating a valid specialization
        """
        specialization = Specialization.objects.create(
            name='Orthodontics',
            description='Specializes in teeth alignment'
        )

        # Verify creation
        assert isinstance(specialization, Specialization)
        assert str(specialization) == 'Orthodontics'

    def test_specialization_required_fields(self):
        """
        Test validation of required fields
        """
        # Test missing name
        with pytest.raises(ValidationError):
            Specialization(description='Test description').full_clean()

    def test_specialization_max_length(self):
        """
        Test name field max length
        """
        # Create a specialization with a name longer than 100 characters
        long_name = 'A' * 101
        
        with pytest.raises(ValidationError):
            Specialization(
                name=long_name,
                description='Test description'
            ).full_clean()

@pytest.mark.django_db
class TestDentistModel:
    def setup_method(self):
        """
        Setup method to create test data
        """
        # Create a user
        self.user = User.objects.create_user(
            username='testdentist',
            email='dentist@example.com',
            password='testpass123'
        )

        # Create a specialization
        self.specialization = Specialization.objects.create(
            name='Pediatric Dentistry',
            description='Specializes in children\'s dental care'
        )

    def test_create_dentist(self):
        """
        Test creating a valid dentist
        """
        dentist = Dentist.objects.create(
            user=self.user,
            specialization=self.specialization,
            license_number='DDS-12345',
            years_of_experience=5
        )

        # Verify creation
        assert isinstance(dentist, Dentist)
        assert str(dentist) == f"Dr. {self.user.get_full_name()}"
        assert dentist.user == self.user
        assert dentist.specialization == self.specialization

    def test_dentist_unique_user(self):
        """
        Test that a user can only be associated with one dentist
        """
        # Create first dentist
        Dentist.objects.create(
            user=self.user,
            specialization=self.specialization,
            license_number='DDS-12345',
            years_of_experience=5
        )

        # Try to create another dentist with the same user
        with pytest.raises(IntegrityError):
            Dentist.objects.create(
                user=self.user,
                specialization=self.specialization,
                license_number='DDS-67890',
                years_of_experience=3
            )

    def test_dentist_unique_license_number(self):
        """
        Test unique constraint on license number
        """
        # Create first dentist
        Dentist.objects.create(
            user=self.user,
            specialization=self.specialization,
            license_number='DDS-12345',
            years_of_experience=5
        )

        # Create another user
        another_user = User.objects.create_user(
            username='anotherdentist',
            email='another@example.com',
            password='testpass123'
        )

        # Try to create another dentist with the same license number
        with pytest.raises(IntegrityError):
            Dentist.objects.create(
                user=another_user,
                specialization=self.specialization,
                license_number='DDS-12345',
                years_of_experience=3
            )

    def test_dentist_nullable_specialization(self):
        """
        Test that specialization can be null
        """
        dentist = Dentist.objects.create(
            user=self.user,
            specialization=None,
            license_number='DDS-67890',
            years_of_experience=7
        )

        assert dentist.specialization is None

    def test_dentist_required_fields(self):
        """
        Test validation of required fields
        """
        # Test missing required fields
        with pytest.raises(ValidationError):
            Dentist(
                user=self.user,
                license_number='DDS-INVALID'
            ).full_clean()

    def test_dentist_years_of_experience_validation(self):
        """
        Test validation of years of experience
        """
        # Test negative years of experience
        with pytest.raises(ValidationError):
            Dentist(
                user=self.user,
                specialization=self.specialization,
                license_number='DDS-NEGATIVE',
                years_of_experience=-1
            ).full_clean()

    def test_dentist_str_method(self):
        """
        Test the string representation of a dentist
        """
        # Create a user with a full name
        user = User.objects.create_user(
            username='fulldentist',
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            password='testpass123'
        )

        dentist = Dentist.objects.create(
            user=user,
            specialization=self.specialization,
            license_number='DDS-FULL',
            years_of_experience=10
        )

        assert str(dentist) == "Dr. John Doe"

# Fixtures for creating test data
@pytest.fixture
def sample_specialization():
    """
    Fixture to create a sample specialization
    """
    return Specialization.objects.create(
        name='Sample Specialization',
        description='Sample description'
    )

@pytest.fixture
def sample_dentist(django_user_model):
    """
    Fixture to create a sample dentist
    """
    user = django_user_model.objects.create_user(
        username='sampledentist',
        email='sample@dentist.com',
        password='testpass123'
    )
    specialization = Specialization.objects.create(
        name='Sample Specialization',
        description='Sample description'
    )
    
    return Dentist.objects.create(
        user=user,
        specialization=specialization,
        license_number='DDS-SAMPLE',
        years_of_experience=5
    )