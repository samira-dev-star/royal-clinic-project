from django.contrib import admin
from .models import ServiceDiscount
# Register your models here.
from django_admin_listfilter_dropdown.filters import DropdownFilter

admin.site.register(ServiceDiscount)
class ServiceDiscountAdmin(admin.ModelAdmin):
    list_display = ('service', 'title', 'discount_percentage', 'start_date', 'end_date', 'is_active')
    list_filter = (
        ('is_active', DropdownFilter),
        ('start_date', DropdownFilter),
        ('end_date', DropdownFilter),
    )
    search_fields = ('title', 'service__service_title')
    list_editable = ('is_active',)
    
    