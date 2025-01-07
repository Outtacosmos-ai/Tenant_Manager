from django.db import models
from apps.patient.models import Patient
from apps.dentist.models import Dentist

class Prescription(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    dentist = models.ForeignKey(Dentist, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    medication = models.CharField(max_length=100)
    dosage = models.CharField(max_length=50)
    frequency = models.CharField(max_length=50)
    duration = models.CharField(max_length=50)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Prescription for {self.patient} - {self.date}"
