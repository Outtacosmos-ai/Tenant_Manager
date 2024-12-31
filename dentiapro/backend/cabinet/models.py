from django.db import models
from core.models import User

class Dentiste(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialite = models.CharField(max_length=100)
    agenda = models.JSONField(default=dict)
    numeroDentiste = models.CharField(max_length=20)

    def __str__(self):
        return self.user.get_full_name()

class Patient(models.Model):
    nomPatient = models.CharField(max_length=100)
    dateNaissance = models.DateField()
    numeroPatient = models.CharField(max_length=20)
    email = models.EmailField()
    historiqueConsultations = models.JSONField(default=list)

    def __str__(self):
        return self.nomPatient