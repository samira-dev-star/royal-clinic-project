from django.db import models
from utils import FileUpload
from django.utils import timezone
from django.utils.html import mark_safe
from django.contrib.admin import display

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
