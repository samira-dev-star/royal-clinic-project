from django.db import models
from apps.accounts.models import Customuser
from apps.services.models import Services
# Create your models here.

class ReserveAppointment(models.Model):
    user = models.ForeignKey(Customuser, on_delete=models.CASCADE, related_name='user_reserve_appointment',verbose_name="کاربر")
    service = models.ForeignKey(Services, on_delete=models.CASCADE, related_name='service_reserve_appointment',verbose_name="خدمات")
    created_at = models.DateTimeField(auto_now_add=True,verbose_name="تاریخ ثبت نوبت")  # زمان رزرو

    def __str__(self):
        return f"{self.user.name} {self.user.family} - {self.service.service_title}"

    class Meta:
        verbose_name = "نوبت رزرو شده"
        verbose_name_plural = "نوبت‌های رزرو شده"