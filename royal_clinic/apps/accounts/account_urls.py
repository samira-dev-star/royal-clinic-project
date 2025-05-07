from django.urls import path
from . import views

app_name = 'account'

urlpatterns =[
    path('register/',views.RegisterUserView.as_view(),name='register'),
    path('rules/',views.show_rules_and_regulations,name='rules'),
    path('login/',views.LoginUser.as_view(),name='login'),
    path('logout/',views.LogoutUserView.as_view(),name='logout'),
    path('userpanel/',views.UserPanelView.as_view(),name='userpanel'),
    path('changepass/',views.ChangePasswordView.as_view(),name='changepass'),
    path('forgotpass/',views.ForgotPasswordView.as_view(),name='forgotpass'),
    path('verifypass/',views.VerifyUserView.as_view(),name='verifypass'),
]