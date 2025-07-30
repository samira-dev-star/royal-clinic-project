from django.db import models

# Create your models here.

from django_jalali.db import models as jmodels
from django.utils import timezone
from apps.services.models import Services
import jdatetime

class ServiceDiscount(models.Model):
    service = models.ManyToManyField(Services, related_name='discounts', verbose_name="سرویس مربوطه")
    title = models.CharField(max_length=200, verbose_name="عنوان تخفیف",null=True, blank=True)
    description = models.TextField(blank=True, null=True, verbose_name="توضیحات")
    
    discount_percentage = models.PositiveIntegerField(verbose_name="درصد تخفیف",null=True, blank=True)
    
    start_date = jmodels.jDateField(verbose_name="شروع تخفیف",null=True, blank=True)
    end_date = jmodels.jDateField(verbose_name="پایان تخفیف",null=True, blank=True)
    
    is_active = models.BooleanField(default=True, verbose_name="فعال باشد؟")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "تخفیف خدمات"
        verbose_name_plural = "تخفیف‌های خدمات"
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.title} - {self.discount_percentage}% برای {self.service}"

    def is_valid_now(self):
        now = timezone.now()
        now_gar = jdatetime.datetime.togregorian(now)
        print(now_gar)
        return self.is_active and self.start_date <= now_gar <= self.end_date
    
    
