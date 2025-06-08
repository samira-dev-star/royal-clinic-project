from django.apps import AppConfig


class PatientPanelConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.patient_panel'
    
    verbose_name = 'پنل بیماران'
    verbose_name_plural = 'پنل بیماران'
    
    def ready(self) -> None:
        from . import signals
        return super().ready()
