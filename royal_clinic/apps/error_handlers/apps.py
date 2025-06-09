from django.apps import AppConfig


class ErrorHandlersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.error_handlers'
    
    verbose_name = 'خطای سیستم'
    verbose_name_plural = 'خطاهای سیستم'
