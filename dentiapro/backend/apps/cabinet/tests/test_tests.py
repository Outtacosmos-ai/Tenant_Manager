import pytest
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.utils import timezone

# Assuming these are your actual models
from apps.tenant.models import Tenant
from apps.cabinet.models import Cabinet

@pytest.mark.django_db
class TestCabinetModel:
    def test_cabinet_creation(self, create_tenant):
        """
        Test basic cabinet creation
        """
        tenant = create_tenant
        
        cabinet = Cabinet.objects.create(
            tenant=tenant,
            name='Test Cabinet',
            address='123 Test St',
            contact_number='+1234567890',
            email='test@cabinet.com',
            is_active=True
        )

        # Verify cabinet creation
        assert isinstance(cabinet, Cabinet)
        assert str(cabinet) == 'Test Cabinet'
        assert cabinet.is_active is True

    def test_cabinet_str_method(self, create_tenant):
        """
        Test the string representation of the cabinet
        """
        tenant = create_tenant
        
        cabinet = Cabinet.objects.create(
            tenant=tenant,
            name='Unique Cabinet',
            address='456 Unique St',
            contact_number='+0987654321',
            email='unique@cabinet.com'
        )

        assert str(cabinet) == 'Unique Cabinet'

    def test_cabinet_required_fields(self, create_tenant):
        """
        Test validation of required fields
        """
        tenant = create_tenant
        
        # Test missing required fields
        with pytest.raises(ValidationError):
            Cabinet.objects.create(
                tenant=tenant,
                name='',  # Empty name
                address='',  # Empty address
                contact_number='',  # Empty contact number
                email=''  # Empty email
            )

    def test_cabinet_email_validation(self, create_tenant):
        """
        Comprehensive email validation tests
        """
        tenant = create_tenant
        
        # Invalid email formats
        invalid_emails = [
            'invalidemail',
            'invalid@',
            '@invalid.com',
            'invalid@invalid',
            'invalid@.com'
        ]

        for email in invalid_emails:
            with pytest.raises(ValidationError):
                cabinet = Cabinet(
                    tenant=tenant,
                    name='Invalid Email Cabinet',
                    address='123 Test St',
                    contact_number='+1234567890',
                    email=email
                )
                cabinet.full_clean()

    def test_contact_number_validation(self, create_tenant):
        """
        Comprehensive contact number validation tests
        """
        tenant = create_tenant
        
        # Invalid contact number formats
        invalid_numbers = [
            '123',  # Too short
            'abcdefghij',  # Non-numeric
            '+123',  # Incomplete number
            '12345678901234567890'  # Too long
        ]

        for number in invalid_numbers:
            with pytest.raises(ValidationError):
                cabinet = Cabinet(
                    tenant=tenant,
                    name='Invalid Number Cabinet',
                    address='123 Test St',
                    contact_number=number,
                    email='test@cabinet.com'
                )
                cabinet.full_clean()

    def test_cabinet_unique_constraints(self, create_tenant):
        """
        Test unique constraints
        """
        tenant = create_tenant
        
        # Create first cabinet
        Cabinet.objects.create(
            tenant=tenant,
            name='First Cabinet',
            address='123 First St',
            contact_number='+1111111111',
            email='first@cabinet.com'
        )

        # Test unique email constraint
        with pytest.raises(IntegrityError):
            Cabinet.objects.create(
                tenant=tenant,
                name='Duplicate Email Cabinet',
                address='456 Second St',
                contact_number='+2222222222',
                email='first@cabinet.com'
            )

    def test_cabinet_default_values(self, create_tenant):
        """
        Test default values for optional fields
        """
        tenant = create_tenant
        
        cabinet = Cabinet.objects.create(
            tenant=tenant,
            name='Default Values Cabinet',
            address='789 Default St',
            contact_number='+3333333333',
            email='default@cabinet.com'
        )

        # Verify default values
        assert cabinet.is_active is False  # Assuming default is False
        assert cabinet.created_at is not None
        assert cabinet.updated_at is not None

    def test_cabinet_active_status_toggle(self, create_tenant):
        """
        Test toggling of active status
        """
        tenant = create_tenant
        
        cabinet = Cabinet.objects.create(
            tenant=tenant,
            name='Status Toggle Cabinet',
            address='101 Toggle St',
            contact_number='+4444444444',
            email='toggle@cabinet.com',
            is_active=False
        )

        # Toggle active status
        cabinet.is_active = True
        cabinet.save()

        # Retrieve and verify
        updated_cabinet = Cabinet.objects.get(id=cabinet.id)
        assert updated_cabinet.is_active is True

    def test_cabinet_tenant_relationship(self, create_tenant):
        """
        Test relationship with tenant
        """
        tenant = create_tenant
        
        cabinet = Cabinet.objects.create(
            tenant=tenant,
            name='Tenant Relationship Cabinet',
            address='202 Relationship St',
            contact_number='+5555555555',
            email='relationship@cabinet.com'
        )

        # Verify tenant relationship
        assert cabinet.tenant == tenant
        assert tenant.cabinet_set.filter(id=cabinet.id).exists()

# Fixtures
@pytest.fixture
def create_tenant():
    """
    Fixture to create a tenant for testing
    """
    return Tenant.objects.create(
        name="Test Tenant",
        domain_url="test.com"
    )

# Optional: Fixture for creating a sample cabinet
@pytest.fixture
def sample_cabinet(create_tenant):
    """
    Fixture to create a sample cabinet
    """
    return Cabinet.objects.create(
        tenant=create_tenant,
        name='Sample Cabinet',
        address='456 Sample St',
        contact_number='+6666666666',
        email='sample@cabinet.com'
    )