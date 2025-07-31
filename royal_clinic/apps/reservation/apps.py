from django.apps import AppConfig


class ReservationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.reservation'
    
    verbose_name = 'رزرو نوبت'
    verbose_name_plural = 'رزرو نوبت‌'
    
    def ready(self):
        import apps.reservation.signals
    