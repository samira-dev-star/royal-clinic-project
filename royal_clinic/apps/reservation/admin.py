from django.contrib import admin
from .models import ReserveAppointment
from django_admin_listfilter_dropdown.filters import DropdownFilter
# Register your models here.

@admin.register(ReserveAppointment)
class ReserveAppointmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'service', 'mobile_number', 'selected_date', 'created_at','is_confirmed')
    list_filter = (('name', DropdownFilter), ('family', DropdownFilter), ('created_at', DropdownFilter))
    search_fields = ['created_at', 'user__name','user__family', 'service__service_title','mobile_number','selected_date']
    list_editable = ['is_confirmed']
    