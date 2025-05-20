from django.db import models
from apps.accounts.models import Customuser
from apps.services.models import Services
from django.core.exceptions import ValidationError

# Create your models here.

class ReserveAppointment(models.Model):
    user = models.ForeignKey(Customuser, on_delete=models.CASCADE, related_name='user_reserve_appointment',verbose_name="کاربر")
    service = models.ForeignKey(Services, on_delete=models.CASCADE, related_name='service_reserve_appointment',verbose_name="خدمات")
    
    name = models.CharField(max_length=50, verbose_name="نام")
    family = models.CharField(max_length=50, verbose_name="نام خانوادگی")
    mobile_number = models.CharField(max_length=13, verbose_name="شماره موبایل")
    
    selected_date = models.CharField(
        max_length=10,
        verbose_name="تاریخ انتخاب"
    )
    created_at = models.DateTimeField(auto_now_add=True,verbose_name="تاریخ ثبت نوبت")  # زمان رزرو
    

    def __str__(self):
        return f"{self.user.name} {self.user.family} - {self.service.service_title}"
    
    # def save(self, *args, **kwargs):
    #     is_new = self._state.adding  # بررسی اینکه شیء تازه ساخته شده یا خیر
        
    #     super().save(*args, **kwargs)
        
    #     if is_new and self.service.capacity is not None:
    #         self.service.capacity = max(self.service.capacity - 1, 0)
    #         self.service.save()
    
    from django.core.exceptions import ValidationError

def save(self, *args, **kwargs):
    is_new_appointment = self._state.adding  # بررسی اینکه شی جدید است یا نه

    # اگر نوبت جدید باشد، اول چک می‌کنیم که ظرفیت پر نباشد
    if is_new_appointment:
        if self.service.capacity is not None and self.service.capacity <= 0:
            raise ValidationError("ظرفیت این سرویس پر شده است.")

    super().save(*args, **kwargs)  # ذخیره‌ی اصلی

    # حالا اگر نوبت جدید بود و سرویس ظرفیت داشت، یکی از ظرفیت کم کنیم
    if is_new_appointment and self.service.capacity is not None:
        self.service.capacity = max(self.service.capacity - 1, 0)
        self.service.save()


def delete(self, *args, **kwargs):
    # اگر ظرفیت سرویس محدود بود، یکی بهش اضافه کنیم
    if self.service.capacity is not None:
        self.service.capacity += 1
        self.service.save()

    super().delete(*args, **kwargs)  # حذف نهایی شیء


    def calq_reservation_capacity(self):
        reservations = 0
        total_capacity = self.service.capacity
        if total_capacity is not None:
            reservations = +total_capacity
        return reservations
        

    class Meta:
        verbose_name = "نوبت رزرو شده"
        verbose_name_plural = "نوبت‌های رزرو شده"
        
        
        
        