# Generated by Django 5.1.1 on 2025-06-07 14:55

import utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient_panel', '0027_alter_custompatient_image_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='custompatient',
            name='image_name',
            field=models.ImageField(blank=True, null=True, upload_to=utils.FileUpload.create_address, verbose_name='تصویر پروفایل'),
        ),
    ]
