from django.shortcuts import render

from apps.accounts.models import Customuser

from django.http import JsonResponse
from .models import Notification
from django.utils import timezone

def get_admin_notifications(request):
    if request.user.is_staff:
        notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')[:10]
        
        notifications_data = []
        for notification in notifications:
            notifications_data.append({
                'message': notification.message,
                'is_read': notification.is_read,
                'timestamp': timezone.localtime(notification.created_at).strftime("%Y-%m-%d %H:%M:%S")
            })
        
        return JsonResponse({'notifications': notifications_data})
    return JsonResponse({'notifications': []})