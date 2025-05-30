from django.contrib import admin
from .models import Personel,PersonelSocialMedia
# Register your models here.


class PersonelAdmin(admin.ModelAdmin):
    list_display = ('name_and_family', 'profession','image')
    search_fields = ('name_and_family', 'profession')
    list_filter = ('profession', 'name_and_family')