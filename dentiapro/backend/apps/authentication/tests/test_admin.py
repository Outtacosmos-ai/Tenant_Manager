import pytest
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from tutorial.quickstart.admin import UserAdmin

@pytest.fixture
def admin_site():
    return AdminSite()

@pytest.fixture
def user_admin(admin_site):
    return UserAdmin(User, admin_site)

@pytest.fixture
def user():
    return User.objects.create(username='testuser')

def test_user_admin_change_view(user_admin, user, rf):
    request = rf.get('/admin/auth/user/1/change/')
    response = user_admin.change_view(request, str(user.id))
    assert response.status_code == 200

def test_user_admin_add_view(user_admin, rf):
    request = rf.get('/admin/auth/user/add/')
    response = user_admin.add_view(request)
    assert response.status_code == 200

def test_user_admin_changelist_view(user_admin, rf):
    request = rf.get('/admin/auth/user/')
    response = user_admin.changelist_view(request)
    assert response.status_code == 200
