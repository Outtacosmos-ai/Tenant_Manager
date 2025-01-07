from django.db import models

class Cabinet(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    contact_number = models.CharField(max_length=20)
    email = models.EmailField()

    def _str_(self):
        return self.name