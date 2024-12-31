from django.db import models
from django_tenants.models import TenantMixin, DomainMixin
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class Cabinet(TenantMixin):
    nomCabinet = models.CharField(max_length=100)
    adresse = models.CharField(max_length=200)
    numTel = models.CharField(max_length=20)
    email = models.EmailField()
    created_on = models.DateField(auto_now_add=True)
    
    auto_create_schema = True

class Domain(DomainMixin):
    pass

class User(AbstractUser):
    email = models.EmailField(unique=True)
    role = models.ForeignKey('Role', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(null=True)
    is_active = models.BooleanField(default=True)

class Role(models.Model):
    role_name = models.CharField(max_length=50)
    description = models.TextField()

class Session(models.Model):
    session_id = models.CharField(max_length=100, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=500)
    expiration = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)

class PasswordReset(models.Model):
    reset_id = models.CharField(max_length=100, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reset_token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()