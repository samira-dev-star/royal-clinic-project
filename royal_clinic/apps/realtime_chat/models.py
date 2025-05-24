from tabnanny import verbose
from django.db import models

class CrispEntryPoint(models.Model):
    class Meta:
        verbose_name = "مشاهده ی پیام ها"
        verbose_name_plural = "مشاهده ی پیام ها"

    def __str__(self):
        return "ورود به پیام ها"
