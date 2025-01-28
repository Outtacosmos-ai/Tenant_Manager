import pytest
from django.contrib.admin import site
from django.contrib.auth import get_user_model
from apps.dentist.admin import DentistAdmin, SpecializationAdmin
from apps.dentist.models import Dentist, Specialization

@pytest.mark.django_db
class TestDentistAdmin:
    def setup_method(self):
        """
        Setup method to initialize test environment
        """
        self.User = get_user_model()
        self.dentist_admin = DentistAdmin(Dentist, site)
        self.specialization_admin = SpecializationAdmin(Specialization, site)

    def create_test_user(self):
        """
        Helper method to create a test user
        """
        return self.User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def create_test_specialization(self):
        """
        Helper method to create a test specialization
        """
        return Specialization.objects.create(
            name='Orthodontics',
            description='Specializes in teeth alignment'
        )

    def test_dentist_admin_registration(self):
        """
        Test that the Dentist model is registered in the admin site
        """
        assert site.is_registered(Dentist)

    def test_specialization_admin_registration(self):
        """
        Test that the Specialization model is registered in the admin site
        """
        assert site.is_registered(Specialization)

    def test_dentist_admin_list_display(self):
        """
        Test the list_display configuration for DentistAdmin
        """
        expected_list_display = ('user', 'specialization', 'license_number')
        
        assert self.dentist_admin.list_display == expected_list_display

    def test_dentist_admin_search_fields(self):
        """
        Test the search_fields configuration for DentistAdmin
        """
        expected_search_fields = ('user_username', 'user_email', 'specialization')
        
        assert self.dentist_admin.search_fields == expected_search_fields

    def test_specialization_admin_list_display(self):
        """
        Test the list_display configuration for SpecializationAdmin
        """
        expected_list_display = ('name', 'description')
        
        assert self.specialization_admin.list_display == expected_list_display

    def test_dentist_admin_list_view(self, admin_client):
        """
        Test the admin list view for dentists
        """
        # Create test data
        user = self.create_test_user()
        specialization = self.create_test_specialization()
        
        Dentist.objects.create(
            user=user,
            specialization=specialization,
            license_number='DDS-12345'
        )

        # Get the admin list view
        url = '/admin/dentist/dentist/'
        response = admin_client.get(url)

        # Assert response
        assert response.status_code == 200
        assert b'testuser' in response.content
        assert b'Orthodontics' in response.content

    def test_specialization_admin_list_view(self, admin_client):
        """
        Test the admin list view for specializations
        """
        # Create test specialization
        self.create_test_specialization()

        # Get the admin list view
        url = '/admin/dentist/specialization/'
        response = admin_client.get(url)

        # Assert response
        assert response.status_code == 200
        assert b'Orthodontics' in response.content
        assert b'Specializes in teeth alignment' in response.content

    def test_dentist_admin_detail_view(self, admin_client):
        """
        Test the admin detail view for a dentist
        """
        # Create test data
        user = self.create_test_user()
        specialization = self.create_test_specialization()
        
        dentist = Dentist.objects.create(
            user=user,
            specialization=specialization,
            license_number='DDS-12345'
        )

        # Get the admin detail view
        url = f'/admin/dentist/dentist/{dentist.id}/change/'
        response = admin_client.get(url)

        # Assert response
        assert response.status_code == 200
        assert b'testuser' in response.content
        assert b'Orthodontics' in response.content

    def test_dentist_admin_filtering(self, admin_client):
        """
        Test admin filtering functionality
        """
        # Create multiple dentists with different specializations
        user1 = self.User.objects.create_user(username='user1', password='pass1')
        user2 = self.User.objects.create_user(username='user2', password='pass2')
        
        spec1 = Specialization.objects.create(name='Orthodontics')
        spec2 = Specialization.objects.create(name='Pediatric Dentistry')
        
        Dentist.objects.create(
            user=user1,
            specialization=spec1,
            license_number='DDS-11111'
        )
        Dentist.objects.create(
            user=user2,
            specialization=spec2,
            license_number='DDS-22222'
        )

        # Get the admin list view with filtering
        url = '/admin/dentist/dentist/?specialization__name=Orthodontics'
        response = admin_client.get(url)

        # Assert response
        assert response.status_code == 200
        assert b'user1' in response.content
        assert b'Orthodontics' in response.content
        assert b'user2' not in response.content

    def test_dentist_admin_search(self, admin_client):
        """
        Test admin search functionality
        """
        # Create test data
        user = self.create_test_user()
        specialization = self.create_test_specialization()
        
        Dentist.objects.create(
            user=user,
            specialization=specialization,
            license_number='DDS-12345'
        )

        # Get the admin list view with search
        url = '/admin/dentist/dentist/?q=testuser'
        response = admin_client.get(url)

        # Assert response
        assert response.status_code == 200
        assert b'testuser' in response.content
        assert b'Orthodontics' in response.content

# Optional: Fixture for creating a dentist (if needed in other tests)
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
        license_number='DDS-SAMPLE'
    )