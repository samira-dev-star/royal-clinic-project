from django.contrib import admin

# Register your models here.

from .models import Notification

@admin.register(Notification)
class NotificationsAdmin(admin.ModelAdmin):
    list_display = ['recipient', 'message', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['message']