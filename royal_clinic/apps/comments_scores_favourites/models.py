from django.db import models
from apps.services.models import Services
from apps.accounts.models import Customuser
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.

class Comment(models.Model):
    service = models.ForeignKey(Services, on_delete=models.CASCADE,related_name='service_comments',verbose_name='سرویس مربوطه')
    
    commenting_user = models.ForeignKey(
        Customuser, 
        on_delete=models.CASCADE,
        related_name='comments_user1',
        verbose_name='کاربر نظر دهنده')
    
    approving_user = models.ForeignKey(
        Customuser, 
        on_delete=models.CASCADE,
        related_name='comments_user2',
        verbose_name='کاربر تایید کننده نظر',
        null=True,
        blank=True)
    
    comment_text = models.TextField(verbose_name='متن نظر')
    
    registerdate = models.DateTimeField(auto_now_add=True,verbose_name='تاریخ درج نظر')
    
    is_active = models.BooleanField(default=False,verbose_name='وضعیت نظر')
    
    comment_parent = models.ForeignKey(
        'Comment',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='والد نظر',
        related_name='comment_child')
    
    is_admin_comment = models.BooleanField(default=False, verbose_name='نظر توسط ادمین')

    # --------------------------------------------------------------
    # اگه فقط خواست که کاربر ادمین بتونه پاسخ کامنت ها رو بده
    
    # def clean(self):
    #     # اگر این کامنت پاسخ به کامنت دیگر باشد
    #     if self.comment_parent and not self.commenting_user.is_staff:
    #         raise ValidationError('فقط کاربران ادمین می‌توانند به نظرات پاسخ دهند.')

    # def save(self, *args, **kwargs):
    #     self.clean()  # فراخوانی دستی clean قبل از ذخیره
    #     super().save(*args, **kwargs)
    # --------------------------------------------------------------
    
    
    
    def __str__(self):
        return f"{self.service} - {self.commenting_user}"
    
    class Meta:
        verbose_name = 'نظر'
        verbose_name_plural = 'نظرات'
        
        
# ------------------------------------------------------------------

class AddScore(models.Model):
    user = models.ForeignKey(Customuser, on_delete=models.CASCADE,verbose_name='کاربر',related_name="scoring_user")
    service = models.ForeignKey(Services, on_delete=models.CASCADE,verbose_name='سرویس',related_name="scoring_service")
    idea = models.TextField(verbose_name='نطر')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')
    
    score = models.PositiveSmallIntegerField(validators=[MinValueValidator(0),MaxValueValidator(5)],verbose_name='امتیاز')
    
    def __str__(self):
        return f"{self.user} - {self.service}"
    
    class Meta:
        verbose_name = 'نطر و امتیاز'
        verbose_name_plural = 'نطرات و امتیازات'