from tabnanny import verbose
from django.db import models

# دلیل ساختنش اینه که جنگو فقط چیزهایی رو توی پنل ادمین نشون می‌ده که مدل باشن.
class CrispEntryPoint(models.Model):
    class Meta:
        verbose_name = "مشاهده ی پیام ها"
        verbose_name_plural = "مشاهده ی پیام ها"

    def __str__(self):
        return "ورود به پیام ها"
