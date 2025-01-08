from django.db import models
from apps.authentication.models import User

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    emergency_contact = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.user.email}"
