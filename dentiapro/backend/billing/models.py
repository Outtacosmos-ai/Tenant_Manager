from django.db import models
from cabinet.models import Patient

class Facture(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    numeroFacture = models.CharField(max_length=20)
    dateEmission = models.DateField()
    montantTotal = models.DecimalField(max_digits=10, decimal_places=2)
    statusPaiement = models.CharField(max_length=20, choices=[
        ('EN_ATTENTE', 'En attente'),
        ('PAYE', 'Payé'),
        ('ANNULE', 'Annulé')
    ])

    def __str__(self):
        return f"Facture {self.numeroFacture} - {self.patient}"