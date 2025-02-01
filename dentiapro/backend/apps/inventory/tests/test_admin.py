import pytest
from django.contrib.admin import site
from django.contrib.auth import get_user_model
from apps.inventory.models import InventoryItem, Category
from apps.inventory.admin import InventoryItemAdmin, CategoryAdmin

@pytest.mark.django_db
class TestInventoryAdmin:
    def setup_method(self):
        """
        Setup method to initialize test environment
        """
        self.User = get_user_model()
        self.inventory_item_admin = InventoryItemAdmin(InventoryItem, site)
        self.category_admin = CategoryAdmin(Category, site)

    def create_test_category(self):
        """
        Helper method to create a test category
        """
        return Category.objects.create(
            name='Test Category',
            description='Test Description'
        )

    def create_test_inventory_item(self, category):
        """
        Helper method to create a test inventory item
        """
        return InventoryItem.objects.create(
            name='Test Item',
            category=category,
            quantity=100,
            cost_price=10.00,
            minimum_quantity=20
        )

    def test_inventory_item_admin_registration(self):
        """
        Test that the InventoryItem model is registered in the admin site
        """
        assert site.is_registered(InventoryItem)

    def test_category_admin_registration(self):
        """
        Test that the Category model is registered in the admin site
        """
        assert site.is_registered(Category)

    def test_inventory_item_admin_list_display(self):
        """
        Test the list_display configuration for InventoryItemAdmin
        """
        expected_list_display = (
            'name', 'category', 'quantity', 'cost_price', 
            'minimum_quantity', 'created_at'
        )
        
        assert self.inventory_item_admin.list_display == expected_list_display

    def test_inventory_item_admin_list_filter(self):
        """
        Test the list_filter configuration for InventoryItemAdmin
        """
        expected_list_filter = ('category', 'created_at')
        
        assert self.inventory_item_admin.list_filter == expected_list_filter

    def test_inventory_item_admin_search_fields(self):
        """
        Test the search_fields configuration for InventoryItemAdmin
        """
        expected_search_fields = ('name', 'category__name')
        
        assert self.inventory_item_admin.search_fields == expected_search_fields

    def test_inventory_item_admin_ordering(self):
        """
        Test the ordering configuration for InventoryItemAdmin
        """
        expected_ordering = ('name',)
        
        assert self.inventory_item_admin.ordering == expected_ordering

    def test_inventory_item_admin_readonly_fields(self):
        """
        Test the readonly_fields configuration for InventoryItemAdmin
        """
        expected_readonly_fields = ('created_at', 'updated_at')
        
        assert self.inventory_item_admin.readonly_fields == expected_readonly_fields

    def test_category_admin_list_display(self):
        """
        Test the list_display configuration for CategoryAdmin
        """
        expected_list_display = ('name', 'description', 'created_at')
        
        assert self.category_admin.list_display == expected_list_display

    def test_category_admin_search_fields(self):
        """
        Test the search_fields configuration for CategoryAdmin
        """
        expected_search_fields = ('name',)
        
        assert self.category_admin.search_fields == expected_search_fields

    def test_category_admin_readonly_fields(self):
        """
        Test the readonly_fields configuration for CategoryAdmin
        """
        expected_readonly_fields = ('created_at', 'updated_at')
        
        assert self.category_admin.readonly_fields == expected_readonly_fields

    def test_inventory_item_admin_list_view(self, admin_client):
        """
        Test the admin list view for inventory items
        """
        # Create test data
        category = self.create_test_category()
        self.create_test_inventory_item(category)

        # Get the admin list view
        url = '/admin/inventory/inventoryitem/'
        response = admin_client.get(url)

        # Assert response
        assert response.status_code == 200
        assert b'Test Item' in response.content
        assert b'Test Category' in response.content

    def test_category_admin_list_view(self, admin_client):
        """
        Test the admin list view for categories
        """
        # Create test category
        self.create_test_category()

        # Get the admin list view
        url = '/admin/inventory/category/'
        response = admin_client.get(url)

        # Assert response
        assert response.status_code == 200
        assert b'Test Category' in response.content
        assert b'Test Description' in response.content

    def test_inventory_item_admin_detail_view(self, admin_client):
        """
        Test the admin detail view for an inventory item
        """
        # Create test data
        category = self.create_test_category()
        inventory_item = self.create_test_inventory_item(category)

        # Get the admin detail view
        url = f'/admin/inventory/inventoryitem/{inventory_item.id}/change/'
        response = admin_client.get(url)

        # Assert response
        assert response.status_code == 200
        assert b'Test Item' in response.content
        assert b'Test Category' in response.content

    def test_inventory_item_admin_filtering(self, admin_client):
        """
        Test admin filtering functionality
        """
        # Create multiple categories and inventory items
        category1 = Category.objects.create(name='Category 1')
        category2 = Category.objects.create(name='Category 2')
        
        InventoryItem.objects.create(
            name='Item 1',
            category=category1,
            quantity=50,
            cost_price=15.00,
            minimum_quantity=10
        )
        InventoryItem.objects.create(
            name='Item 2',
            category=category2,
            quantity=75,
            cost_price=20.00,
            minimum_quantity=15
        )

        # Get the admin list view with filtering
        url = '/admin/inventory/inventoryitem/?category__name=Category 1'
        response = admin_client.get(url)

        # Assert response
        assert response.status_code == 200
        assert b'Item 1' in response.content
        assert b'Category 1' in response.content
        assert b'Item 2' not in response.content

    def test_inventory_item_admin_search(self, admin_client):
        """
        Test admin search functionality
        """
        # Create test data
        category = self.create_test_category()
        self.create_test_inventory_item(category)

        # Get the admin list view with search
        url = '/admin/inventory/inventoryitem/?q=Test Item'
        response = admin_client.get(url)

        # Assert response
        assert response.status_code == 200
        assert b'Test Item' in response.content
        assert b'Test Category' in response.content

# Optional: Fixture for creating an inventory item (if needed in other tests)
@pytest.fixture
def sample_inventory_item():
    """
    Fixture to create a sample inventory item
    """
    category = Category.objects.create(
        name='Sample Category',
        description='Sample description'
    )
    
    return InventoryItem.objects.create(
        name='Sample Item',
        category=category,
        quantity=50,
        cost_price=25.00,
        minimum_quantity=10
    )