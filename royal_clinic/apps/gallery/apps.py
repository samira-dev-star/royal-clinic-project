from django.apps import AppConfig


class GalleryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.gallery'
    
    verbose_name = 'گالری'
    verbose_name_plural = 'گالری'
    
    def ready(self) -> None:
        from . import signals
        return super().ready()
