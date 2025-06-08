from turtle import mode
from django.db import models
from django.contrib import admin
from utils import FileUpload
from django.utils import timezone
from django.utils.html import mark_safe
from django.contrib.admin import display
from ckeditor_uploader.fields import RichTextUploadingField
from utils import FileUpload

# mark safe is similar to httpresponse >> both take an html code in string format and run it.
# Create your models here.

class Sliders(models.Model):
    slider_title1 = models.CharField(max_length=500,null=True,blank=True,verbose_name="متن اول")
    slider_title2 = models.CharField(max_length=500,null=True,blank=True,verbose_name="متن دوم")
    slider_title3 = models.CharField(max_length=500,null=True,blank=True,verbose_name="متن سوم")
    
    file_upload = FileUpload('images','sliders')
    
    image_name = models.ImageField(upload_to=file_upload.create_address,verbose_name="تصویر اسلایدر")
    
    slider_link = models.URLField(max_length=200,null=True,blank=True,verbose_name="لینک")
    
    is_active = models.BooleanField(default=True,blank=True,verbose_name="وضعیت فعال/غیرفعال")
    
    register_date = models.DateTimeField(auto_now_add=True,verbose_name="تاریخ درج")
    publish_date = models.DateTimeField(default=timezone.now,verbose_name="تاریخ انتشار")
    update_date = models.DateTimeField(auto_now=True,verbose_name="تاریخ اخرین بروزرسانی")
    
    def __str__(self):
        return f"{self.slider_title1}"
    
    class Meta:
        verbose_name = "اسلایدر"
        verbose_name_plural = "اسلایدر ها"
        
    @display(description="تصویر اسلاید")
    def image_slide(self):
        return mark_safe(f'<img src="/media/{self.image_name}" style="width:80px; height:80px"/>')
    
    
    
    # میخوام لینک اسلایدر از توی پنل ادمین هم قابل کلیک کردن باشه
    def link(self):
        return mark_safe(f'<a href="{self.slider_link} target="_blank">link</a>')
    
    link.short_description = 'پیوندها'
    
    
    
# ----------------------------------------------------------------------

class SocialMediaAddresses(models.Model):
    SOCIAL_NAMES = (
        ('تلگرام', 'تلگرام'),
        ('اینستاگرام', 'اینستاگرام'),
        ('واتساپ', 'واتساپ'),
        ('لینکدین', 'لینکدین'),
        ('یوتیوب', 'یوتیوب'),
    )

    social_name = models.CharField(max_length=100,null=True,blank=True,verbose_name="نام شبکه",choices=SOCIAL_NAMES)
    social_link = models.URLField(max_length=200,null=True,blank=True,verbose_name="لینک شبکه")
    
    is_active = models.BooleanField(default=True,blank=True,verbose_name="وضعیت فعال/غیرفعال")
    
    register_date = models.DateTimeField(auto_now_add=True,verbose_name="تاریخ درج")
    publish_date = models.DateTimeField(default=timezone.now,verbose_name="تاریخ انتشار")
    update_date = models.DateTimeField(auto_now=True,verbose_name="تاریخ اخرین بروزرسانی")
    
    def __str__(self):
        return f"{self.social_name}"
    
    class Meta:
        verbose_name = "آدرس شبکه"
        verbose_name_plural = "آدرس های شبکه"
    
    @display(description="لینک شبکه")
    def link(self):
        return mark_safe(f'<a href="{self.social_link} target="_blank">link</a>')
    
    link.short_description = 'پیوندها'
    
    
# ----------------------------------------------------------------------


        
        

class IndexIntroduction(models.Model):
    heading = models.CharField(max_length=500,null=True,blank=True,verbose_name="سرتیتر")
    title = models.CharField(max_length=500,null=True,blank=True,verbose_name="عنوان")
    introduction = RichTextUploadingField(null=True,blank=True,verbose_name="معرفی سایت",config_name='special')
    
    file_upload = FileUpload('images','index')
    image = models.FileField(upload_to=file_upload.create_address,verbose_name="مدیا",null=True,blank=True)
    
    
    
    def __str__(self):
        return f"{self.title}"
    
    @admin.display(description='مدیا')
    def show_media_in_admin(self):
        return mark_safe(f'<img src="/media/{self.image}" style="width:80px; height:80px"/>')
    
    class Meta:
        verbose_name = "معرفی سایت"
        verbose_name_plural = "معرفی سایت"
    

# ----------------------------------------------------------------------



class Properties(models.Model):
    properties = models.ForeignKey(IndexIntroduction,null=True,blank=True,verbose_name="امکانات",on_delete=models.CASCADE,related_name='propertiess')
    name = models.CharField(max_length=400,null=True,blank=True,verbose_name="نام ویژگی")
    
    def __str__(self):
        return f"{self.properties}"
    
    class Meta:
        verbose_name = "ویژگی"
        verbose_name_plural = "ویژگی ها"