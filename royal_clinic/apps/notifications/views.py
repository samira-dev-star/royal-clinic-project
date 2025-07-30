from django.shortcuts import render
from django.http import JsonResponse
from .models import Notification
from apps.accounts.models import Customuser
# Create your views here.

from django.views.decorators.http import require_GET
from django.views.decorators.csrf import csrf_exempt  # فقط اگر AJAX با CSRF مشکل داشت

@require_GET
def get_admin_notifications(request):
    if request.user.is_authenticated and request.user.is_staff:
        notifs = Notification.objects.filter(recipient=request.user, is_read=False)
        notif_list = list(notifs.values('id', 'message', 'created_at'))

        # بلافاصله بعد از ارسال، نوتیف‌ها رو read کنیم
        notifs.update(is_read=True)

        return JsonResponse({'notifications': notif_list})
    return JsonResponse({'notifications': []})
