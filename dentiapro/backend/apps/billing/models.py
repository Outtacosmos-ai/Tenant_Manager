from django.db import models
from apps.patient.models import Patient

class Invoice(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=50, blank=True, null=True)
    payment_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"Invoice {self.id} - {self.patient}"
