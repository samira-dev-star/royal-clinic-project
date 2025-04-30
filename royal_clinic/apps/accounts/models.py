from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
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


class Customuser(AbstractBaseUser):
    mobile_number = models.CharField(max_length=11,unique=True)
    unique_code = models.UUIDField(default=uuid4,null=False,blank=False,unique=True)
    email = models.EmailField(max_length=200,blank=True)
    name = models.CharField(max_length=50,blank=True)
    family = models.CharField(max_length=50,blank=True)
    GENDER = (
    ('', 'انتخاب نشده'),
    ('مرد', 'مرد'),
    ('زن', 'زن'),
    )
    gender = models.CharField(max_length=50, blank=True, choices=GENDER, default='',null=True)
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
    
    
    