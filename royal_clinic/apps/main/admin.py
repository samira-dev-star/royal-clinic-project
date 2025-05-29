from django.contrib import admin

from .models import Sliders,SocialMediaAddresses
# Register your models here.

# deactivation action
def de_active_slider(modeladmin, request, queryset):
    res = queryset.update(is_active=False)
    message = f"تعداد {res} اسلایدر غیر فعال شد"
    modeladmin.message_user(request, message)

@admin.register(Sliders)
class SliderAdmin(admin.ModelAdmin):
    list_display = ['image_slide','slider_title1','link','is_active','register_date',]
    list_filter = ['slider_title1',]
    search_fields = ['slider_title1',]
    ordering = ['update_date',]
    readonly_fields = ['image_slide',]
    actions = [de_active_slider,]
    list_editable = ['is_active',]
    
    
# ----------------------------------------------

@admin.register(SocialMediaAddresses)
class SocialMediaAddressesAdmin(admin.ModelAdmin):
    list_display = ['social_name','link','is_active','register_date',]
    list_filter = ['social_name',]
    search_fields = ['social_name',]
    ordering = ['update_date',]
    list_editable = ['is_active',]