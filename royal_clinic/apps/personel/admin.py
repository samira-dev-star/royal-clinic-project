from django.contrib import admin
from .models import Personel,PersonelSocialMedia
# Register your models here.

class PersonelSocialMediaInline(admin.TabularInline):
    model = PersonelSocialMedia
    

@admin.register(Personel)
class PersonelAdmin(admin.ModelAdmin):
    list_display = ('show_personel_images','name_and_family', 'profession')
    search_fields = ('name_and_family', 'profession')
    list_filter = ('profession', 'name_and_family')
    inlines = [PersonelSocialMediaInline]