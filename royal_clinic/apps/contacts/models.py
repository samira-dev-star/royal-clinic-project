from django.db import models
from django.utils import timezone


# Create your models here.


class Contact(models.Model):
    email1 = models.EmailField(
        max_length=50,
        verbose_name='ایمیل ۱',
        null=True,
        blank=True
    )
    email2 = models.EmailField(
        max_length=50,
        verbose_name='ایمیل ۲',
        null=True,
        blank=True
    )
    mobile_number1 = models.CharField(
        max_length=11,
        verbose_name='شماره موبایل ۱',
        null=True,
        blank=True
    )
    mobile_number2 = models.CharField(
        max_length=11,
        verbose_name='شماره موبایل ۲',
        null=True,
        blank=True
    )
    address = models.CharField(
        max_length=300,
        verbose_name='آدرس کلینیک',
        null=True,
        blank=True
    )
    

    def __str__(self):
        return f"اطلاعات تماس: { self.mobile_number1 }"

    class Meta:
        verbose_name = 'اطلاعات تماس کلینیک'
        verbose_name_plural = 'اطلاعات تماس‌ کلینیک'

    
