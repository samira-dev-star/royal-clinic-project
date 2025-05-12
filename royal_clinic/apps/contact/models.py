from django.db import models
from django.utils import timezone


# Create your models here.


class Contact(models.Model):
    email1 = models.EmailField(
        max_length=50,
        verbose_name='ایمیل ۱',
        blank=True,
        default=""
    )
    email2 = models.EmailField(
        max_length=50,
        verbose_name='ایمیل ۲',
        blank=True,
        default=""
    )
    mobile_number1 = models.CharField(
        max_length=13,
        verbose_name='شماره موبایل ۱',
        blank=True,
        default=""
    )
    mobile_number2 = models.CharField(
        max_length=13,
        verbose_name='شماره موبایل ۲',
        blank=True,
        default=""
    )
    address = models.CharField(
        max_length=300,
        verbose_name='آدرس کلینیک',
        blank=True
    )
    

    def __str__(self):
        return f"اطلاعات تماس: { self.mobile_number1 }"

    class Meta:
        verbose_name = 'اطلاعات تماس کلینیک'
        verbose_name_plural = 'اطلاعات تماس‌ کلینیک'

    
# ----------------------------------------------------------------

class WorkingTimesType1(models.Model):
    DAYS = (
        ('شنبه', 'شنبه'),
        ('یکشنبه', 'یکشنبه'),
        ('دوشنبه', 'دوشنبه'),
        ('سه شنبه', 'سه شنبه'),
        ('چهارشنبه', 'چهارشنبه'),
        ('پنجشنبه', 'پنجشنبه'),
        ('جمعه', 'جمعه'),
        
    )
    day = models.CharField(
        max_length=10,
        verbose_name='روز',
        choices=DAYS,
        null=True,
        blank=True
    )
    
    
    start_time = models.TimeField(
        verbose_name='زمان شروع',
        blank=True,
        null=True,
    )
    end_time = models.TimeField(
        verbose_name='زمان پایان',
        blank=True,
        null=True,
    )
    
    
    
    def __str__(self):
        return f"روز: { self.day } - { self.start_time } - { self.end_time }"
    
    class Meta:
        verbose_name = 'ساعت کاری'
        verbose_name_plural = 'ساعات کاری'
        
    
# ----------------------------------------------------------------

class WorkingTimeType2(models.Model):

    day = models.CharField(
        max_length=30,
        verbose_name='روز',
        null=True,
        blank=True,
    )
    
    
    time_state = models.CharField(
        max_length=20,
        verbose_name='زمان شروع',
        blank=True,
        default="",
    )
    
    
    
    def __str__(self):
        return f"روز: { self.day } - { self.time_state }"
    
    class Meta:
        verbose_name = 'ساعت کاری مدل 2'
        verbose_name_plural = 'ساعات کاری مدل 2'

# --------------------------------------------------------------------------------------------

# users public messages to clinic

class ContactMessage(models.Model):
    name = models.CharField(max_length=100,verbose_name='نام و نام خانوادگی')
    email = models.EmailField(verbose_name='ایمیل',null=True,blank=True)
    phone = models.CharField(max_length=20,verbose_name='شماره موبایل')
    message = models.TextField(verbose_name='پیام')
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='تاریخ ارسال')

    def __str__(self):
        return f"پیام از {self.name}"
