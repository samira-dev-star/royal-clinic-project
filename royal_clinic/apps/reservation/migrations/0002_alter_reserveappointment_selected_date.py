# Generated by Django 5.1.1 on 2025-05-18 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserveappointment',
            name='selected_date',
            field=models.DateField(help_text='لطفا در بین بازه تاریخی تایید شده زمانی راانتخاب کنید', verbose_name='تاریخ انتخاب'),
        ),
    ]
