from django.db import models
from django.contrib.auth.models import User

class Dentist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    speciality = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50)

    def __str__(self):
        return self.user.get_full_name()
