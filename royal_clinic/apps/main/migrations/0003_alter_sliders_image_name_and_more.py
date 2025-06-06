# Generated by Django 5.1.1 on 2025-05-30 03:56

import utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_socialmediaaddresses_alter_sliders_image_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sliders',
            name='image_name',
            field=models.ImageField(upload_to=utils.FileUpload.create_address, verbose_name='تصویر اسلایدر'),
        ),
        migrations.AlterField(
            model_name='socialmediaaddresses',
            name='social_name',
            field=models.CharField(blank=True, choices=[('تلگرام', 'تلگرام'), ('اینستاگرام', 'اینستاگرام'), ('واتساپ', 'واتساپ'), ('لینکدین', 'لینکدین'), ('یوتیوب', 'یوتیوب')], max_length=100, null=True, verbose_name='نام شبکه'),
        ),
    ]
