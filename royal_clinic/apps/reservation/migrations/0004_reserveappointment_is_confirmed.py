# Generated by Django 5.1.1 on 2025-05-25 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0003_alter_reserveappointment_selected_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='reserveappointment',
            name='is_confirmed',
            field=models.BooleanField(default=False, verbose_name='تایید شده'),
        ),
    ]
