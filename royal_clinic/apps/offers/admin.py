from django.contrib import admin
from .models import ServiceDiscount
# Register your models here.
from django_admin_listfilter_dropdown.filters import DropdownFilter
from django.forms import widgets
from apps.services.models import Services


class ServiceDiscountAdmin(admin.ModelAdmin):
    list_display = ( 'title', 'discount_percentage', 'start_date', 'end_date', 'is_active')
    list_filter = (
        ('is_active', DropdownFilter),
        ('start_date', DropdownFilter),
        ('end_date', DropdownFilter),
    )
    search_fields = ('title', 'service__service_title')
    list_editable = ('is_active',)
    
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'service':
            kwargs['queryset'] = Services.objects.filter(is_available=True)
            kwargs['widget'] = widgets.CheckboxSelectMultiple()
            kwargs['help_text'] = 'مشخص بفرمائید که چه سرویس هایی شامل این تخفیف هستند'
        return super().formfield_for_manytomany(db_field, request, **kwargs)
    
    
    

admin.site.register(ServiceDiscount, ServiceDiscountAdmin)
