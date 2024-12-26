from django.db import models
from clinics.models import Dentist
from patients.models import Patient

class Appointment(models.Model):
    dentist = models.ForeignKey(Dentist, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    reason = models.TextField()

    def __str__(self):
        return f"{self.patient} - {self.date_time}"
