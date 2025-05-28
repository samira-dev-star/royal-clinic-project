from django.db import models
from apps.accounts.models import Customuser
from utils import FileUpload
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib import admin
import django_jalali.db.models as jmodels
# Create your models here.

class CustomPatient(models.Model):
    user = models.OneToOneField(Customuser, on_delete=models.CASCADE, primary_key=True, verbose_name='کاربر',related_name='patient')
    address = models.TextField(null=True, blank=True, verbose_name='آدرس')
    birth_date = models.DateField(default=timezone.now,null=True, blank=True, verbose_name='تاریخ تولد')
    
    blood_type = models.CharField(max_length=3, choices=[('A+', 'A+'),('A-', 'A-'),('O+', 'O+'), ('O-', 'O-'),('B+','B+'),('B-','B-'),('AB+', 'AB+'),('AB-', 'AB-')], blank=True, null=True, verbose_name='گروه خونی')
    
    
    height = models.PositiveIntegerField(
    null=True,
    blank=True,
    verbose_name='قد (سانتی‌متر)',   
    help_text='قد بیمار به سانتی‌متر'
    )

    weight = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='وزن (کیلوگرم)',
        help_text='وزن بیمار به کیلوگرم'
    )

    
    emergency_contact = models.CharField(max_length=13, blank=True, null=True, verbose_name='شماره تماس اضطراری',help_text='021-12345678')
    
    file_upload = FileUpload('images', 'patients')
    image_name = models.ImageField(upload_to=file_upload.create_address, verbose_name='تصویر پروفایل', null=True, blank=True)

    def __str__(self):
        return f"{self.user}"
    
    @admin.display(description='سن')
    def get_age(self):
        if self.birth_date:
            return (timezone.now().date() - self.birth_date).days // 365
        return None
    

    
    class Meta:
        verbose_name = 'بیمار'
        verbose_name_plural = 'بیماران'




class Allergy(models.Model):
    patient = models.ForeignKey(CustomPatient, on_delete=models.CASCADE, related_name='allergies', verbose_name='بیمار')
    title = models.CharField(max_length=100, verbose_name='عنوان حساسیت',null=True, blank=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'حساسیت'
        verbose_name_plural = 'حساسیت ها'


class MedicalHistoryItem(models.Model):
    patient = models.ForeignKey(CustomPatient, on_delete=models.CASCADE, related_name='medical_history_items', verbose_name='بیمار')
    title = models.CharField(max_length=200, verbose_name='عنوان بیماری یا سابقه',null=True, blank=True)
    description = models.TextField(blank=True, null=True, verbose_name='توضیحات')
    diagnosis_year = models.IntegerField(default=timezone.now,blank=True, null=True, verbose_name='تاریخ تشخیص')

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'بیماری یا سابقه'
        verbose_name_plural = 'بیماری یا سابقه'



class CurrentMedications(models.Model):
    patient = models.ForeignKey(CustomPatient, on_delete=models.CASCADE, related_name='medications', verbose_name='بیمار')
    medication_name = models.CharField(max_length=100, verbose_name='نام دارو',null=True, blank=True)
    dosage = models.CharField(max_length=100, verbose_name='دوز مصرف',null=True, blank=True)
    priscribed_at = models.DateField(default=timezone.now, verbose_name='تاریخ شروع مصرف',null=True, blank=True)
    USING_STATE = (
        ('در حال استفاده', 'در حال استفاده'),
        ('مصرف تمام شده', 'مصرف تمام شده'),
    )
    using_state = models.CharField(max_length=20, choices=USING_STATE, default='still_using', verbose_name='وضعیت استفاده')
   

    def __str__(self):
        return self.medication_name
    
    class Meta:
        verbose_name = 'دارو'
        verbose_name_plural = 'داروها'
        
        
        
class ShowPatientPanelForAdmin(models.Model):
    class Meta:
        verbose_name = 'نمایش پنل و اطلاعات بیماران'
        verbose_name_plural = 'نمایش پنل و اطلاعات بیماران'
        
    def __str__(self):
        return "نمایش پنل و اطلاعات بیماران"