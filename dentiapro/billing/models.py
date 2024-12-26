from django.db import models

# Create your models here.
from django.db import models
from patients.models import Patient

class Invoice(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Invoice {self.id} - {self.patient}"
    