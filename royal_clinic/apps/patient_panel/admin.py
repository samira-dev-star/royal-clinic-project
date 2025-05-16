from django.contrib import admin
from .models import CustomPatient
from django_admin_listfilter_dropdown.filters import DropdownFilter
# Register your models here.



@admin.register(CustomPatient)
class CustomPatientAdmin(admin.ModelAdmin):
    list_display = ('user','emergency_contact','get_age','height','weight','blood_type','address')
    search_fields = ('get_age','height','weight','blood_type')
    list_filter = (('height',DropdownFilter),('weight',DropdownFilter),('blood_type',DropdownFilter))
    
