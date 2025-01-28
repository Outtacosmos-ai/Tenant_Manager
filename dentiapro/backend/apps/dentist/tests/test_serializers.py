import pytest
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from decimal import Decimal

# Assuming these are your actual models and serializers
from apps.dentist.models import Dentist, Specialization
from apps.dentist.serializers import (
    SpecializationSerializer, 
    DentistSerializer
)

@pytest.mark.django_db
class TestSpecializationSerializer:
    def test_create_valid_specialization(self):
        """
        Test creating a valid specialization
        """
        valid_data = {
            'name': 'Orthodontics',
            'description': 'Specializes in teeth alignment'
        }

        serializer = SpecializationSerializer(data=valid_data)
        assert serializer.is_valid(), serializer.errors

        # Save the serializer
        specialization = serializer.save()
        
        # Verify saved data
        assert specialization.name == 'Orthodontics'
        assert specialization.description == 'Specializes in teeth alignment'

    def test_specialization_required_fields(self):
        """
        Test validation of required fields
        """
        # Test missing name
        invalid_data = {
            'description': 'Test description'
        }

        serializer = SpecializationSerializer(data=invalid_data)
        assert not serializer.is_valid()
        assert 'name' in serializer.errors

    def test_specialization_max_length(self):
        """
        Test name field max length validation
        """
        # Create data with name longer than 100 characters
        invalid_data = {
            'name': 'A' * 101,
            'description': 'Test description'
        }

        serializer = SpecializationSerializer(data=invalid_data)
        assert not serializer.is_valid()
        assert 'name' in serializer.errors

@pytest.mark.django_db
class TestDentistSerializer:
    def setup_method(self):
        """
        Setup method to create test data
        """
        # Create a user
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            username='testdentist',
            email='dentist@example.com',
            password='testpass123',
            first_name='John',
            last_name='Doe'
        )

        # Create a specialization
        self.specialization = Specialization.objects.create(
            name='Pediatric Dentistry',
            description='Specializes in children\'s dental care'
        )

    def test_create_valid_dentist(self):
        """
        Test creating a valid dentist
        """
        # Create a dentist
        dentist = Dentist.objects.create(
            user=self.user,
            specialization=self.specialization,
            license_number='DDS-12345',
            years_of_experience=5
        )

        # Serialize the dentist
        serializer = DentistSerializer(dentist)
        
        # Verify serialized data
        assert serializer.data['user'] == str(self.user)
        assert serializer.data['specialization']['name'] == 'Pediatric Dentistry'
        assert serializer.data['license_number'] == 'DDS-12345'
        assert serializer.data['years_of_experience'] == 5

    def test_dentist_serializer_fields(self):
        """
        Test the fields in the DentistSerializer
        """
        # Create a dentist
        dentist = Dentist.objects.create(
            user=self.user,
            specialization=self.specialization,
            license_number='DDS-12345',
            years_of_experience=5
        )

        # Serialize the dentist
        serializer = DentistSerializer(dentist)
        
        # Verify serialized data fields
        expected_fields = [
            'id', 'user', 'specialization', 
            'license_number', 'years_of_experience'
        ]
        assert set(serializer.data.keys()) == set(expected_fields)

    def test_dentist_serializer_nested_specialization(self):
        """
        Test nested specialization serialization
        """
        # Create a dentist
        dentist = Dentist.objects.create(
            user=self.user,
            specialization=self.specialization,
            license_number='DDS-12345',
            years_of_experience=5
        )

        # Serialize the dentist
        serializer = DentistSerializer(dentist)
        
        # Verify nested specialization data
        assert 'specialization' in serializer.data
        assert serializer.data['specialization']['name'] == 'Pediatric Dentistry'
        assert serializer.data['specialization']['description'] == 'Specializes in children\'s dental care'

    def test_dentist_serializer_nullable_specialization(self):
        """
        Test serialization with null specialization
        """
        # Create a dentist with no specialization
        dentist = Dentist.objects.create(
            user=self.user,
            specialization=None,
            license_number='DDS-67890',
            years_of_experience=7
        )

        # Serialize the dentist
        serializer = DentistSerializer(dentist)
        
        # Verify serialized data
        assert serializer.data['specialization'] is None

    def test_dentist_serializer_validation(self):
        """
        Test dentist serializer validation
        """
        # Attempt to create a dentist with invalid data
        invalid_data = {
            'user': self.user.id,
            'license_number': 'DDS-INVALID',
            # Missing years_of_experience
        }

        serializer = DentistSerializer(data=invalid_data)
        assert not serializer.is_valid()
        assert 'years_of_experience' in serializer.errors

    def test_dentist_serializer_years_of_experience_validation(self):
        """
        Test validation of years of experience
        """
        # Create a dentist
        dentist = Dentist.objects.create(
            user=self.user,
            specialization=self.specialization,
            license_number='DDS-12345',
            years_of_experience=5
        )

        # Attempt to update with invalid years of experience
        invalid_data = {
            'years_of_experience': -1
        }

        serializer = DentistSerializer(dentist, data=invalid_data, partial=True)
        assert not serializer.is_valid()
        assert 'years_of_experience' in serializer.errors

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

# Parametrized tests for additional scenarios
@pytest.mark.parametrize('input_data,expected_validity', [
    # Valid data
    ({
        'name': 'Orthodontics',
        'description': 'Teeth alignment specialist'
    }, True),
    # Invalid data (missing name)
    ({
        'description': 'Test description'
    }, False),
    # Invalid data (name too long)
    ({
        'name': 'A' * 101,
        'description': 'Test description'
    }, False)
])
def test_specialization_serializer_variations(input_data, expected_validity):
    """
    Parametrized test for specialization serializer
    """
    serializer = SpecializationSerializer(data=input_data)
    assert serializer.is_valid() == expected_validity