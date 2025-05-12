from django.contrib import admin
from jalali_date.admin import ModelAdminJalaliMixin
from .models import Contact,WorkingTimesType1,WorkingTimeType2,ContactMessage
# Register your models here.

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['mobile_number1', 'email1' , 'address']
    list_filter = ['mobile_number1']
    search_fields = ['mobile_number1']
    
    
    
@admin.register(WorkingTimesType1)
class WorkingTimesAdmin(ModelAdminJalaliMixin,admin.ModelAdmin):
    list_display = ['day', 'start_time', 'end_time']
    list_filter = ['day']
    search_fields = ['day']
    ordering = ['day']
    


@admin.register(WorkingTimeType2)
class WorkingTimeAdmin2(admin.ModelAdmin):
    list_display = ['day', 'time_state']
    list_filter = ['day']
    search_fields = ['day']
    ordering = ['day']


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'message', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'email', 'phone', 'message']
    ordering = ['-created_at']
    
