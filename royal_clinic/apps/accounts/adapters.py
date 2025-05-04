# accounts/adapters.py
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from .models import Customuser

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        # تنظیم mobile_number از داده‌های شبکه اجتماعی (اگر وجود ندارد، از ایمیل استفاده کنید)
        user.mobile_number = sociallogin.account.extra_data.get('phone_number', '') or sociallogin.account.extra_data.get('email', '')
        return user