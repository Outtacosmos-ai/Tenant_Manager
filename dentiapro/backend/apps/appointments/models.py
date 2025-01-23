from django.db import models
from apps.users.models import User  # Correct import

class Appointment(models.Model):
    tenant = models.ForeignKey('tenant.Tenant', on_delete=models.CASCADE)  # Ensure app name is correct
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    dentist = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments_as_dentist')
    date = models.DateField()
    start_time = models.TimeField()
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"Appointment with {self.dentist} for {self.patient} on {self.date}"
