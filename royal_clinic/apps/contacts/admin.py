from django.contrib import admin
from .models import Contact
# Register your models here.

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['mobile_number1', 'email1' , 'address']
    list_filter = ['mobile_number1']
    search_fields = ['mobile_number1']
    