# Generated by Django 5.1.1 on 2025-05-07 13:54

import ckeditor.fields
import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Services',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_title', models.CharField(max_length=150, verbose_name='عنوان خدمات')),
                ('service_short_description', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='شرح کوتاه')),
                ('service_description', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='شرح طولانی')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(blank=True, unique=True)),
            ],
            options={
                'verbose_name': 'خدمات کلینیک',
                'verbose_name_plural': 'خدمات کلینیک',
            },
        ),
    ]
