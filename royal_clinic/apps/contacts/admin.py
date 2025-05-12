from django.contrib import admin
from .models import Contact,WorkingTimesType1,WorkingTimeType2
# Register your models here.

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['mobile_number1', 'email1' , 'address']
    list_filter = ['mobile_number1']
    search_fields = ['mobile_number1']
    
    
    
@admin.register(WorkingTimesType1)
class WorkingTimesAdmin(admin.ModelAdmin):
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
