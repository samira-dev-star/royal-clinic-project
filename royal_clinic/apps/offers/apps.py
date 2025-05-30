from django.apps import AppConfig


class OffersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.offers'
    
    verbose_name = 'تخفیف'
    verbose_name_plural = 'تخفیف ها'
