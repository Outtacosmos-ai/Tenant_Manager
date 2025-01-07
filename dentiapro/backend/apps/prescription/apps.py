from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Prescription

@receiver(post_save, sender=Prescription)
def prescription_created(sender, instance, created, **kwargs):
    if created:
        # Handle new prescription logic here
        pass
