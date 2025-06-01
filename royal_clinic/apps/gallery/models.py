from django.db import models
from utils import FileUpload
from apps.services.models import Services  # فرض اینکه مدل Service قبلاً وجود داره

class ServiceVideo(models.Model):
    service = models.ForeignKey(Services, on_delete=models.CASCADE, related_name='videos', verbose_name='سرویس مربوطه',null=True,blank=True)
    title = models.CharField(max_length=200, verbose_name='عنوان ویدیو',null=True, blank=True)
    description = models.TextField(blank=True, null=True, verbose_name='توضیحات')
    
    file_upload_videos = FileUpload('videos', 'services')
    video_file = models.FileField(upload_to=file_upload_videos.create_address, verbose_name='فایل ویدیو')
    
    file_upload_thumbnails = FileUpload('videos', 'thumbnails')
    thumbnail = models.ImageField(upload_to=file_upload_thumbnails.create_address, blank=True, null=True, verbose_name='تصویر شاخص')
    
    upload_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ آپلود')
    is_active = models.BooleanField(default=True, verbose_name='فعال باشد؟')

    class Meta:
        verbose_name = 'ویدیو سرویس'
        verbose_name_plural = 'ویدیوهای سرویس'

    def __str__(self):
        return f"{self.title} ({self.service.title})"
