from django.db import models
from apps.patient.models import Patient
from apps.dentist.models import Dentist

class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    dentist = models.ForeignKey(Dentist, on_delete=models.CASCADE)
    date = models.DateField()
    diagnosis = models.TextField()
    treatment = models.TextField()
    notes = models.TextField(blank=True)

    def _str_(self):
        return f"Medical Record for {self.patient} - {self.date}"