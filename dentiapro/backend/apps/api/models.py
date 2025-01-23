from django.db import models

class TimestampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class ExampleTenantRelatedModel(TimestampMixin):
    name = models.CharField(max_length=255)
    tenant = models.ForeignKey('tenant.Tenant', on_delete=models.CASCADE, related_name='example_models')  # Fix reference

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Example Model"
        verbose_name_plural = "Example Models"
