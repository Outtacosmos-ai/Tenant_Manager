from django.db import models
from apps.patient.models import Patient
from apps.dentist.models import Dentist

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    dentist = models.ForeignKey(Dentist, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=[
        ('SCHEDULED', 'Scheduled'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
        ('COMPLETED', 'Completed')
    ], default='SCHEDULED')

    def __str__(self):
        return f"{self.patient} - {self.date_time}"
