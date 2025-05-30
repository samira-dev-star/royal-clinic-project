from django.db import models
from apps.accounts.models import Customuser
from utils import FileUpload
from django.utils.html import mark_safe
from django.contrib.admin import display
# Create your models here.


class Personel(models.Model):
    user = models.ForeignKey(Customuser, on_delete=models.CASCADE, related_name='user_personel',verbose_name="کاربر")
    profession = models.CharField(max_length=255, verbose_name="شغل",null=True, blank=True)
    name_and_family = models.CharField(max_length=255, verbose_name="نام و نام خانوادگی")
    description = models.TextField(verbose_name="توضیحات",null=True, blank=True)
    
    file_upload = FileUpload('images', 'personel')
    image = models.ImageField(upload_to=file_upload.create_address, verbose_name="تصویر",null=True, blank=True)
    
    class Meta:
        verbose_name = "تیم متخصص"
        verbose_name_plural = "تیم متخصص"
        
    def __str__(self):
        return self.name_and_family
    
    @display(description='تصویر پرسنل')
    def show_personel_images(self):
        return mark_safe(f'<img src="/media/{self.image}" width="100" height="100" />')
    
    
    
    
class PersonelSocialMedia(models.Model):
    personel = models.ForeignKey(Personel, on_delete=models.CASCADE, related_name='personel_social_media',verbose_name="تیم متخصص")
    
    SOCIAL_MEDIA = (
        ('email', 'email'),
        ('instagram', 'instagram'),
        ('linkedin', 'linkedin'),
    )
    social_media = models.CharField(max_length=255, verbose_name="سایت", choices=SOCIAL_MEDIA, null=True, blank=True)
    media_link = models.CharField(max_length=255, verbose_name="لینک", null=True, blank=True)
    
    class Meta:
        verbose_name = "آدرس شبکه های اجتماعی"
        verbose_name_plural = "آدرس شبکه های اجتماعی"
        
    def __str__(self):
        return self.social_media
    
    @display(description='لینک شبکه')
    def link(self):
        return mark_safe(f'<a href="{self.media_link} target="_blank">link</a>')
    