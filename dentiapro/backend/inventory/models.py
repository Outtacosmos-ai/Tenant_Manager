from django.db import models

class Stock(models.Model):
    nomProduit = models.CharField(max_length=100)
    quantite = models.IntegerField()
    seuilMin = models.IntegerField()

    def __str__(self):
        return self.nomProduit