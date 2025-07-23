from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.utils import timezone
from uuid import uuid4

# Create your models here.


class CustomUserManager(BaseUserManager):
                   
    def create_user(self,mobile_number,email="",name="",family="",gender=None,password=None): 
        if not mobile_number:
            raise ValueError('شماره موبایل باید وارد شود')
        
        user = self.model(
            mobile_number = mobile_number,
            email = self.normalize_email(email),
            name = name,
            family = family,
            gender = gender,
        )
        
        user.set_password(password)
        
        user.save(using=self._db) # yani in user ro baraye estefade dar database zaxire kon.
        return user

    def create_superuser(self,mobile_number,email,name,family,password=None,gender=None):
        user = self.create_user(
            mobile_number=mobile_number,
            email=email, # email hayi ke karbar vared karde ro normal mikone.
            name=name,
            family=family,
            gender=gender,
            password=password
            )
        user.is_active = True
        user.is_admin = True
        # ke hamun lahze ke super user saxte mishe in ro True kone
        user.is_superuser = True
        
        user.save(using=self._db)
        return user
# 


class Customuser(AbstractBaseUser,PermissionsMixin):
    mobile_number = models.CharField(max_length=13,unique=True,help_text='لطفا شماره موبایل خود را درست وارد فرمائید',verbose_name='شماره موبایل')
    unique_code = models.UUIDField(default=uuid4,null=False,blank=False,unique=True)
    email = models.EmailField(max_length=200,blank=True,verbose_name='ایمیل')
    name = models.CharField(max_length=50,blank=True,verbose_name='نام')
    family = models.CharField(max_length=50,blank=True,verbose_name='نام خانوادگی')
    
    GENDER = (
    ('', 'انتخاب نشده'),
    ('مرد', 'مرد'),
    ('زن', 'زن'),
    )
    gender = models.CharField(max_length=50, blank=True, choices=GENDER, default='',null=True, verbose_name='جنسیت')
    
    registered_date = models.DateField(default=timezone.now)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    

    
    USERNAME_FIELD = 'mobile_number'
    REQUIRED_FIELDS = ['email','name','family']
    
    @property
    def is_staff(self):
        return self.is_admin
    
    objects = CustomUserManager()
    
    def __str__(self):
        return self.name+" "+self.family
    class Meta:
        verbose_name = "کاربران و پرسنل"
        verbose_name_plural = "کاربران و پرسنل"


    def get_full_name(self):
        return f"{self.name} {self.family}".strip()


from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField

    
class RulesandRegulations(models.Model):
    rules_and_conditions = RichTextUploadingField(null=True,blank=True,verbose_name='قوانین و مقررات',config_name='special')
    registered_date = models.DateField(auto_now_add=True,verbose_name='تاریخ ثبت')
    last_checked = models.DateTimeField(auto_now=True,verbose_name='اخرین بازدید')
    is_active = models.BooleanField(default=False,verbose_name='فعال/غیرفعال')
    
    def __str__(self):
        return str(self.registered_date)
    
    class Meta:
        verbose_name = "قوانین و مقررات"
        verbose_name_plural = "قوانین و مقررات"
        
        
# ----------------------------------------------------------------------------------------------------------------------------

from datetime import timedelta
from django.conf import settings

class ActivationCode(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='activation_codes')
    code = models.CharField(max_length=100,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)
    
    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=5)  # انقضا بعد از 5 دقیقه

    def __str__(self):
        return f"{self.user.mobile_number} - {self.code}"
