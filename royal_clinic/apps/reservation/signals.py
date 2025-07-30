from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ReserveAppointment
from apps.notifications.models import Notification
from apps.accounts.models import Customuser

@receiver(post_save, sender=ReserveAppointment)
def create_notification_for_admin(sender, instance, created, **kwargs):
    if created:
        admins = Customuser.objects.filter(is_staff=True)
        for admin in admins:
            Notification.objects.create(
                recipient=admin,
                message=f"نوبت جدید توسط {instance.user.name} {instance.user.family} رزرو شد."
            )
