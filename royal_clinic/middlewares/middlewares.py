# accounts/middleware.py
# from django.contrib.auth import logout
# from django.contrib import messages
# from django.shortcuts import redirect

# class SessionSecurityMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         if request.user.is_authenticated:
#             session_ip = request.session.get('ip_address')
#             session_ua = request.session.get('user_agent')
#             current_ip = request.META.get('REMOTE_ADDR')
#             current_ua = request.META.get('HTTP_USER_AGENT')

#             if session_ip != current_ip or session_ua != current_ua:
#                 logout(request)
#                 messages.warning(request, "امنیت حساب شما به خطر افتاد، دوباره وارد شوید.")
#                 return redirect('accounts:login')  # مسیر ورود

#         return self.get_response(request)


