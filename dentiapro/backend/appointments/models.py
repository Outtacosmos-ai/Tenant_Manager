from django.db import models
from cabinet.models import Dentiste, Patient

class RendezVous(models.Model):
    dentiste = models.ForeignKey(Dentiste, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateField()
    heure = models.TimeField()
    statusRendezVous = models.CharField(max_length=20, choices=[
        ('PLANIFIE', 'Planifié'),
        ('CONFIRME', 'Confirmé'),
        ('ANNULE', 'Annulé'),
        ('TERMINE', 'Terminé')
    ])

    def __str__(self):
        return f"{self.patient} - {self.date} {self.heure}"