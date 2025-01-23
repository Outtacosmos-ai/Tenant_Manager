from django.db import models

# Create your models here.

from django.db import models

# Utility mixin for timestamp fields
class TimestampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

# Example of models that would fit this app context.
class ExampleTenantRelatedModel(TimestampMixin):
    name = models.CharField(max_length=255)
    tenant = models.ForeignKey('apps.tenants.Tenant', on_delete=models.CASCADE, related_name='example_models')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Example Model"
        verbose_name_plural = "Example Models"
