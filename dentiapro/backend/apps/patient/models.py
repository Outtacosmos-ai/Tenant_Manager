from django.db import models
from apps.authentication.models import User

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    emergency_contact = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Patient"
        verbose_name_plural = "Patients"

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.user.email}"

    def clean(self):
        from django.core.exceptions import ValidationError
        if not self.phone_number.isdigit():
            raise ValidationError("Phone number must contain only digits.")
        if len(self.phone_number) < 10:
            raise ValidationError("Phone number must be at least 10 digits long.")
