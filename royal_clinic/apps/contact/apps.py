from django.apps import AppConfig


class ContactConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.contact'

    verbose_name = 'اطلاعات تماس کلینیک'
    verbose_name_plural = 'اطلاعات تماس‌ کلینیک'