from django.db import models
from apps.accounts.models import Customuser
from apps.services.models import Services
from django.core.exceptions import ValidationError
from django_jalali.db import models as jmodels
from django.db.models import F
from django.db import transaction

# Create your models here.

class ReserveAppointment(models.Model):
    user = models.ForeignKey(Customuser, on_delete=models.CASCADE, related_name='user_reserve_appointment',verbose_name="کاربر")
    service = models.ForeignKey(Services, on_delete=models.CASCADE, related_name='service_reserve_appointment',verbose_name="خدمات")
    
    name = models.CharField(max_length=50, verbose_name="نام")
    family = models.CharField(max_length=50, verbose_name="نام خانوادگی")
    mobile_number = models.CharField(max_length=13, verbose_name="شماره موبایل")
    
    selected_date = jmodels.jDateField(verbose_name='تاریخ انتخاب‌ شده',null=True,blank=True)
    

    created_at = models.DateTimeField(auto_now_add=True,verbose_name="تاریخ ثبت نوبت")  # زمان رزرو
    is_confirmed = models.BooleanField(default=False, verbose_name="تایید شده")
    
    
    def clean(self):
        """
        بررسی اینکه تاریخ انتخاب‌ شده در بازه تاریخی سرویس باشه.
        """
        if self.service and self.selected_date:
            start = self.service.start_reservation_date
            end = self.service.finish_reservation_date

            if not (start <= self.selected_date <= end):
                from django.core.exceptions import ValidationError
                raise ValidationError({
                    'selected_date': f'تاریخ انتخاب‌شده باید بین {start} تا {end} باشد.'
                })
    

    def __str__(self):
        return f"{self.user.name} {self.user.family} - {self.service.service_title}"
    
   

    # when a new appointment is made we need to decrease the capacity of the service
    def save(self, *args, **kwargs):
        is_new_appointment = self._state.adding
        if is_new_appointment:
            service = Services.objects.get(pk=self.service.pk)
            if service.capacity is not None:
                service.capacity = max(service.capacity - 1, 0)
                print(service.capacity)
                service.save()
        super().save(*args, **kwargs) 
        
    
    
    # def delete(self, *args, **kwargs):
    #     # اول ظرفیت سرویس رو افزایش بده
    #     if self.service.capacity is not None:
    #         service = Services.objects.get(pk=self.service.pk)
    #         service.capacity+=1
    #         service.save()
    #     # سپس نوبت رو حذف کن
    #     super().delete(*args, **kwargs)


    # def delete(self, *args, **kwargs):
    #     # اگر ظرفیت سرویس محدود بود، یکی بهش اضافه کنیم
    #     if self.service.capacity is not None:
    #         self.service.capacity += 1
    #         self.service.save()

    #     super().delete(*args, **kwargs)  # حذف نهایی شیء


    def calq_reservation_capacity(self):
        reservations = 0
        total_capacity = self.service.capacity
        if total_capacity is not None:
            reservations = +total_capacity
        return reservations
        

    class Meta:
        verbose_name = "نوبت رزرو شده"
        verbose_name_plural = "نوبت‌های رزرو شده"
        
        
        
        