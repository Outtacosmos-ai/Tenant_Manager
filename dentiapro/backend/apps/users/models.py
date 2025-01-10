from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('dentist', 'Dentist'),
        ('patient', 'Patient'),
        ('staff', 'Staff'),
    )
    
    tenant = models.ForeignKey('tenant.Tenant', on_delete=models.CASCADE, related_name='users')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    class Meta:
        db_table = 'users'
        ordering = ['username']

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"