import pytest
from django.contrib.admin import site
from django.contrib.auth import get_user_model
from django.test import RequestFactory
from apps.cabinet.admin import CabinetAdmin
from apps.cabinet.models import Cabinet

@pytest.mark.django_db
class TestCabinetAdmin:
    def setup_method(self):
        """
        Setup method to initialize test environment
        """
        self.model = Cabinet
        self.admin_class = CabinetAdmin
        self.User = get_user_model()

    def create_superuser(self):
        """
        Helper method to create a superuser
        """
        return self.User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='testpass123'
        )

    def create_test_cabinet(self):
        """
        Helper method to create a test cabinet
        """
        return Cabinet.objects.create(
            name='Test Cabinet',
            address='123 Test Street',
            contact_number='+1234567890',
            email='test@cabinet.com',
            is_active=True
        )

    def test_admin_registration(self):
        """
        Test that the Cabinet model is registered in the admin site
        """
        assert site.is_registered(self.model)

    def test_admin_list_display(self):
        """
        Test the list_display configuration
        """
        expected_list_display = (
            'name', 'address', 'contact_number', 
            'email', 'is_active', 'created_at'
        )
        
        admin_instance = self.admin_class(self.model, site)
        assert admin_instance.list_display == expected_list_display

    def test_admin_search_fields(self):
        """
        Test the search_fields configuration
        """
        expected_search_fields = ('name', 'email')
        
        admin_instance = self.admin_class(self.model, site)
        assert admin_instance.search_fields == expected_search_fields

    def test_admin_list_filter(self):
        """
        Test the list_filter configuration
        """
        expected_list_filter = ('is_active', 'created_at')
        
        admin_instance = self.admin_class(self.model, site)
        assert admin_instance.list_filter == expected_list_filter

    def test_admin_readonly_fields(self):
        """
        Test the readonly_fields configuration
        """
        expected_readonly_fields = ('created_at', 'updated_at')
        
        admin_instance = self.admin_class(self.model, site)
        assert admin_instance.readonly_fields == expected_readonly_fields

    def test_admin_cabinet_list_view(self):
        """
        Test the admin list view for cabinets
        """
        # Create a superuser and log in
        superuser = self.create_superuser()
        
        # Create some test cabinets
        cabinets = [
            self.create_test_cabinet(),
            self.create_test_cabinet()
        ]

        # Create a request factory
        request_factory = RequestFactory()
        request = request_factory.get('/admin/cabinets/cabinet/')
        request.user = superuser

        # Create admin instance
        admin_instance = self.admin_class(self.model, site)

        # Get the changelist
        changelist = admin_instance.get_changelist(request)
        
        # Verify the changelist
        assert changelist is not None

    def test_admin_cabinet_detail_view(self):
        """
        Test the admin detail view for a cabinet
        """
        # Create a superuser and log in
        superuser = self.create_superuser()
        
        # Create a test cabinet
        cabinet = self.create_test_cabinet()

        # Create a request factory
        request_factory = RequestFactory()
        request = request_factory.get(f'/admin/cabinets/cabinet/{cabinet.id}/change/')
        request.user = superuser

        # Create admin instance
        admin_instance = self.admin_class(self.model, site)

        # Get the form
        form = admin_instance.get_form(request, cabinet)
        
        # Verify the form
        assert form is not None

    def test_admin_cabinet_filtering(self):
        """
        Test admin filtering functionality
        """
        # Create test cabinets with different statuses
        Cabinet.objects.create(
            name='Active Cabinet',
            is_active=True,
            email='active@cabinet.com'
        )
        Cabinet.objects.create(
            name='Inactive Cabinet',
            is_active=False,
            email='inactive@cabinet.com'
        )

        # Create a superuser
        superuser = self.create_superuser()

        # Create a request factory
        request_factory = RequestFactory()
        request = request_factory.get('/admin/cabinets/cabinet/', {'is_active__exact': '1'})
        request.user = superuser

        # Create admin instance
        admin_instance = self.admin_class(self.model, site)

        # Get the changelist
        changelist = admin_instance.get_changelist(request)
        
        # Verify filtering
        queryset = changelist.get_queryset(request)
        assert queryset.count() > 0
        assert all(cabinet.is_active for cabinet in queryset)

    def test_admin_search_functionality(self):
        """
        Test admin search functionality
        """
        # Create test cabinets
        Cabinet.objects.create(
            name='Search Cabinet',
            email='search@cabinet.com'
        )

        # Create a superuser
        superuser = self.create_superuser()

        # Create a request factory
        request_factory = RequestFactory()
        request = request_factory.get('/admin/cabinets/cabinet/', {'q': 'Search'})
        request.user = superuser

        # Create admin instance
        admin_instance = self.admin_class(self.model, site)

        # Get the changelist
        changelist = admin_instance.get_changelist(request)
        
        # Verify search
        queryset = changelist.get_queryset(request)
        assert queryset.count() > 0
        assert any('Search' in str(cabinet.name) for cabinet in queryset)

# Optional: Fixture for creating a cabinet (if needed in other tests)
@pytest.fixture
def sample_cabinet():
    """
    Fixture to create a sample cabinet
    """
    return Cabinet.objects.create(
        name='Sample Cabinet',
        address='456 Sample Street',
        contact_number='+0987654321',
        email='sample@cabinet.com',
        is_active=True
    )