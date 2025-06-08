from django.apps import AppConfig


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.main'
    
    verbose_name = 'صفحه ی اصلی'
    verbose_name_plural = 'صفحه ی اصلی'
    
    def ready(self) -> None:
        from . import signals
        return super().ready()
