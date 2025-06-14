from django.apps import AppConfig


class ServicesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.services'
    
    verbose_name = "خدمات کلینیک"
    verbose_name_plural = "خدمات کلینیک"
    
    def ready(self) -> None:
        from . import signals
        return super().ready()
