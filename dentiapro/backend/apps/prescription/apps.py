from django.apps import AppConfig

class PrescriptionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.prescription'
    verbose_name = 'Prescription Management'

    def ready(self):
        import apps.prescription.signals  # noqa

