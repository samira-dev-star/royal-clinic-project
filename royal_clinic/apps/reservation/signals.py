from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import ReserveAppointment
from apps.accounts.models import Customuser

from apps.services.models import Services  # اگر مدل سرویس جای دیگه‌ست
# مسیر بالا رو با توجه به ساختار پروژه خودت تغییر بده

# اگر created == True باشد: یعنی این اولین بار است که این نمونه (مثلاً ReserveAppointment) در دیتابیس ذخیره شده (یعنی آبجکت جدید است).

# اگر created == False باشد: یعنی این آبجکت قبلاً وجود داشته و فقط به‌روزرسانی شده است.



@receiver(post_delete, sender=ReserveAppointment)
def increase_service_capacity_on_delete(sender, instance, **kwargs):
    service = Services.objects.get(id=instance.service.id)
    if service.capacity is not None:
        service.capacity += 1
        service.save()