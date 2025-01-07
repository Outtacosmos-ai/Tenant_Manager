from django.db import models
from apps.core.models import User

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    address = models.TextField()
    phone = models.CharField(max_length=20)
    emergency_contact = models.CharField(max_length=100)
    medical_history = models.TextField(blank=True)

    def __str__(self):
        return self.user.get_full_name()

