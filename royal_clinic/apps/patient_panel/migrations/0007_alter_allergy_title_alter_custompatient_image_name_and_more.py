# Generated by Django 5.1.1 on 2025-05-16 14:19

import django.db.models.deletion
import utils
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient_panel', '0006_alter_custompatient_image_name_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='allergy',
            name='title',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='عنوان حساسیت'),
        ),
        migrations.AlterField(
            model_name='custompatient',
            name='image_name',
            field=models.ImageField(blank=True, null=True, upload_to=utils.FileUpload.create_address, verbose_name='تصویر پروفایل'),
        ),
        migrations.AlterField(
            model_name='custompatient',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='patient', serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='کاربر'),
        ),
        migrations.AlterField(
            model_name='medicalhistoryitem',
            name='title',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='عنوان بیماری یا سابقه'),
        ),
    ]
