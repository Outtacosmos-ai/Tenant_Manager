from django.db import models
from apps.core.models import User

class Specialization(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def _str_(self):
        return self.name

class Dentist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.ForeignKey(Specialization, on_delete=models.SET_NULL, null=True)
    license_number = models.CharField(max_length=50, unique=True)
    years_of_experience = models.PositiveIntegerField()

    def _str_(self):
        return f"Dr. {self.user.get_full_name()}"