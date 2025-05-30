from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from utils import FileUpload

from django.utils import timezone
from django.utils.text import slugify

from django.urls import reverse
from django.db.models import Q

# Create your models here.

class Services(models.Model):
    service_title = models.CharField(max_length=150,verbose_name='عنوان خدمات')
    service_short_description = RichTextField(verbose_name='شرح کوتاه',null=True,blank=True,config_name='special')
    service_description = RichTextUploadingField(verbose_name='شرح طولانی',null=True,blank=True,config_name='special')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True)
    
    image_uploader = FileUpload('images','service_images')
    service_image = models.ImageField(upload_to=image_uploader.create_address,verbose_name='تصویر خدمات',null=True,blank=True)
    
    is_available = models.BooleanField(verbose_name='فعال/غیرفعال',null=True,blank=True)
    
    start_reservation_date =  models.DateTimeField(default=timezone.now,verbose_name='تاریخ شروع نوبت دهی')
    finish_reservation_date =  models.DateTimeField(default=timezone.now,verbose_name='تاریخ پایان نوبت دهی')
    
    capacity = models.IntegerField(verbose_name='ظرفیت نوبت',null=True,blank=True)
    proper_candidate_description = RichTextField(verbose_name='شرح شرایط کاندید',null=True,blank=True,config_name='special')
    
    
    procedure_description = RichTextField(verbose_name='شرح کلی پروسه این سرویس ',null=True,blank=True,config_name='special')
    
    def get_absolute_url(self):
        return reverse("services:service_detail", kwargs={"slug": self.slug})
    
    # متد __str__ باید فقط یک رشته (str) برگردونه.
    def __str__(self):
        return f"{self.service_title}"
    
    # ولی save() یا delete() متدهایی هستن که وظیفه انجام کار (side effect) دارن، نه برگردوندن نتیجه.
    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.service_title)
        super().save(*args, **kwargs)
    
    # دابل آندرلاین (__) برای فیلتر کردن یا annotate کردن در QuerySet استفاده می‌شه،
    # هر شی از مدل Service، می‌تونه به همه‌ی تخفیف‌های مربوط به خودش با self.discounts دسترسی داشته
    @property  
    def has_discount(self):
            return self.discounts.filter(Q(is_active=True) & Q(start_date__lte=timezone.now()) & Q(end_date__gte=timezone.now())).exists()
            
    @property
    def current_discount(self):
        now = timezone.now()
        return self.discounts.filter(
            is_active=True,
            start_date__lte=now,
            end_date__gte=now
        ).first()

    
    class Meta:
        verbose_name = "خدمات کلینیک"
        verbose_name_plural = "خدمات کلینیک"
        
# -----------------------------------------------------------------------------------
   
class ServiceFeatures(models.Model):
    service = models.ForeignKey(
        Services,
        on_delete=models.CASCADE,
        related_name='features',
        verbose_name='خدمات مرتبط'
    )
    feature_name = models.CharField(max_length=100, verbose_name='نام ویژگی',null=True,blank=True)
    feature_value = models.CharField(max_length=255, verbose_name='مقدار ویژگی',null=True,blank=True)

    def __str__(self):
        return f"{self.feature_name}: {self.feature_value}"

    class Meta:
        verbose_name = "ویژگی خدمات"
        verbose_name_plural = "ویژگی‌های خدمات"


# -----------------------------------------------------------------------------------

class ServiceAdvantages(models.Model):
    service = models.ForeignKey(
        Services,
        on_delete=models.CASCADE,
        related_name='advantages',
        verbose_name='مزایای این سرویس'
    )
    advantage_name = models.CharField(max_length=100, verbose_name='نام مزیت',null=True,blank=True)
    advantage_value = models.CharField(max_length=255, verbose_name='صفت مزیت',null=True,blank=True)
    
    

    def __str__(self):
        return f"{self.advantage_name}: {self.advantage_value}"

    class Meta:
        verbose_name = "مزایای خدمات"
        verbose_name_plural = "مزایای خدمات"
        

# -----------------------------------------------------------------------------------

class ServiceCandidateCondition(models.Model):
    service = models.ForeignKey(
        Services,
        on_delete=models.CASCADE,
        related_name='conditions',
        verbose_name='شرایط استفاده کننده از این سرویس'
    )
    condition = models.CharField(max_length=400, verbose_name='شرایط',null=True,blank=True)
    
    

    def __str__(self):
        return f"{self.condition}"

    class Meta:
        verbose_name = "شرایط استفاده از این خدمات"
        verbose_name_plural = "شرایط استفاده از این خدمات"
        
# -----------------------------------------------------------------------------------

class ServiceProcedures(models.Model):
    service = models.ForeignKey(
        Services,
        on_delete=models.CASCADE,
        related_name='procedures',
        verbose_name='پروسه'
    )
    process_name = models.CharField(max_length=200, verbose_name='نام مراحل',null=True,blank=True)
    process = models.CharField(max_length=500, verbose_name='توضیح مراحل',null=True,blank=True)
    
    

    def __str__(self):
        return f"{self.process_name}"

    class Meta:
        verbose_name = "مراحل استفاده از این خدمات"
        verbose_name_plural = "مراحل استفاده از این خدمات"
        
# -----------------------------------------------------------------------------------

class ServiceRecurringQuestion(models.Model):
    service = models.ForeignKey(
        Services,
        on_delete=models.CASCADE,
        related_name='recurring_questions',
        verbose_name='سوالات متداول درباره ی این سرویس'
    )
    question = models.CharField(max_length=200, verbose_name='سوال')
    answer = RichTextField(verbose_name='پاسخ',null=True,blank=True,config_name='special')

    def __str__(self):
        return f"{self.service} - {self.question}"

    class Meta:
        verbose_name = "سوال متداول سرویس"
        verbose_name_plural = "سوالات متداول سرویس"

# ---------------------------------------------------------------------------

