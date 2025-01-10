from django.db import models
from apps.tenant.models import Tenant
from apps.users.models import User

class MedicalRecord(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='medical_records')
    dentist = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_medical_records')
    diagnosis = models.TextField()
    treatment_plan = models.TextField()
    notes = models.TextField(blank=True)
    attachments = models.FileField(upload_to='medical_records/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'medical_records'
        ordering = ['-created_at']
        verbose_name = 'Medical Record'
        verbose_name_plural = 'Medical Records'

    def __str__(self):
        return f"Medical Record for {self.patient} on {self.created_at.date()}"
