import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

# Assuming these are your actual models
from apps.dentist.models import Dentist, Specialization
from apps.core.models import User

@pytest.mark.django_db
class TestDentistModelCreation:
    def setup_method(self):
        """
        Setup method to create test data
        """
        # Create a user
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            username='dentist', 
            password='testpass123',
            first_name='John',
            last_name='Doe'
        )

        # Create a specialization
        self.specialization = Specialization.objects.create(
            name='Orthodontics', 
            description='Teeth alignment'
        )

    def test_dentist_creation(self):
        """
        Test creating a valid dentist
        """
        dentist = Dentist.objects.create(
            user=self.user,
            specialization=self.specialization,
            license_number='DEN12345',
            years_of_experience=5
        )

        # Verify dentist creation
        assert isinstance(dentist, Dentist)
        assert str(dentist) == f"Dr. {self.user.get_full_name()}"

    def test_dentist_unique_user(self):
        """
        Test that a user can only be associated with one dentist
        """
        # Create first dentist
        Dentist.objects.create(
            user=self.user,
            specialization=self.specialization,
            license_number='DEN12345',
            years_of_experience=5
        )

        # Create another user
        another_user = self.User.objects.create_user(
            username='another_dentist', 
            password='testpass456'
        )

        # Try to create another dentist with the same user
        with pytest.raises(Exception):
            Dentist.objects.create(
                user=self.user,  # Attempting to use the same user
                specialization=self.specialization,
                license_number='DEN67890',
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
            license_number='DEN12345',
            years_of_experience=5
        )

        # Create another user
        another_user = self.User.objects.create_user(
            username='another_dentist', 
            password='testpass456'
        )

        # Try to create another dentist with the same license number
        with pytest.raises(Exception):
            Dentist.objects.create(
                user=another_user,
                specialization=self.specialization,
                license_number='DEN12345',  # Same license number
                years_of_experience=3
            )

    def test_dentist_nullable_specialization(self):
        """
        Test that specialization can be null
        """
        dentist = Dentist.objects.create(
            user=self.user,
            specialization=None,
            license_number='DEN67890',
            years_of_experience=7
        )

        assert dentist.specialization is None

    def test_dentist_years_of_experience_validation(self):
        """
        Test validation of years of experience
        """
        # Test negative years of experience
        with pytest.raises(ValidationError):
            invalid_dentist = Dentist(
                user=self.user,
                specialization=self.specialization,
                license_number='DEN_INVALID',
                years_of_experience=-1
            )
            invalid_dentist.full_clean()

    def test_dentist_str_method(self):
        """
        Test the string representation of a dentist
        """
        # Create a user with a full name
        user = self.User.objects.create_user(
            username='fulldentist',
            first_name='Jane',
            last_name='Smith',
            password='testpass789'
        )

        dentist = Dentist.objects.create(
            user=user,
            specialization=self.specialization,
            license_number='DEN_FULL',
            years_of_experience=10
        )

        assert str(dentist) == "Dr. Jane Smith"

    def test_dentist_required_fields(self):
        """
        Test validation of required fields
        """
        # Create another user
        another_user = self.User.objects.create_user(
            username='requiredfields', 
            password='testpass000'
        )

        # Test missing required fields
        with pytest.raises(ValidationError):
            invalid_dentist = Dentist(
                user=another_user,
                # Missing specialization and license_number
            )
            invalid_dentist.full_clean()

# Fixtures for creating test data
@pytest.fixture
def sample_user(django_user_model):
    """
    Fixture to create a sample user
    """
    return django_user_model.objects.create_user(
        username='sampleuser',
        email='sample@example.com',
        password='testpass123'
    )

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
def sample_dentist(sample_user, sample_specialization):
    """
    Fixture to create a sample dentist
    """
    return Dentist.objects.create(
        user=sample_user,
        specialization=sample_specialization,
        license_number='DEN_SAMPLE',
        years_of_experience=5
    )

# Parametrized tests for additional scenarios
@pytest.mark.parametrize('years_of_experience,is_valid', [
    (0, True),    # Zero years of experience
    (5, True),    # Positive years of experience
    (-1, False),  # Negative years of experience
    (100, True)   # Large number of years
])
def test_dentist_years_of_experience_variations(
    sample_user, 
    sample_specialization, 
    years_of_experience, 
    is_valid
):
    """
    Parametrized test for years of experience
    """
    try:
        dentist = Dentist.objects.create(
            user=sample_user,
            specialization=sample_specialization,
            license_number=f'DEN_{years_of_experience}',
            years_of_experience=years_of_experience
        )
        assert is_valid, f"Expected invalid for {years_of_experience} years"
    except Exception:
        assert not is_valid, f"Expected valid for {years_of_experience} years"