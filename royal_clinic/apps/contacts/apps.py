from django.apps import AppConfig


class ContactsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.contacts'

    verbose_name = 'اطلاعات تماس کلینیک'
    verbose_name_plural = 'اطلاعات تماس‌ کلینیک'