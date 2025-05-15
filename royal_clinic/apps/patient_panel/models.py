from django.db import models
from apps.accounts.models import Customuser
from utils import FileUpload
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.

class CustomPatient(models.Model):
    user = models.OneToOneField(Customuser, on_delete=models.CASCADE, primary_key=True, verbose_name='کاربر',related_name='patient')
    address = models.TextField(null=True, blank=True, verbose_name='آدرس')
    birth_date = models.DateField(default=timezone.now,null=True, blank=True, verbose_name='تاریخ تولد')
    
    blood_type = models.CharField(max_length=3, choices=[('A+', 'A+'),('A-', 'A-'),('O+', 'O+'), ('O-', 'O-'),('B+','B+'),('B-','B-'),('AB+', 'AB+'),('AB-', 'AB-')], blank=True, null=True, verbose_name='گروه خونی')
    
    
    height = models.PositiveIntegerField(
    null=True,
    blank=True,
    verbose_name='قد (سانتی‌متر)',  # بهتره واحد هم بنویسی
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
    
    class Meta:
        verbose_name = 'بیمار'
        verbose_name_plural = 'بیماران'




class Allergy(models.Model):
    patient = models.ForeignKey(CustomPatient, on_delete=models.CASCADE, related_name='allergies', verbose_name='بیمار')
    title = models.CharField(max_length=100, verbose_name='عنوان حساسیت')

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'حساسیت'
        verbose_name_plural = 'حساسیت ها'


class MedicalHistoryItem(models.Model):
    patient = models.ForeignKey(CustomPatient, on_delete=models.CASCADE, related_name='medical_history_items', verbose_name='بیمار')
    title = models.CharField(max_length=200, verbose_name='عنوان بیماری یا سابقه')
    description = models.TextField(blank=True, null=True, verbose_name='توضیحات')
    diagnosis_year = models.IntegerField(default=timezone.now,blank=True, null=True, verbose_name='تاریخ تشخیص')

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'بیماری یا سابقه'
        verbose_name_plural = 'بیماری یا سابقه'
