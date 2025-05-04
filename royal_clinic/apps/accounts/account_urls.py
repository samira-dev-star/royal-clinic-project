from django.urls import path
from . import views

app_name = 'account'

urlpatterns =[
    path('register/',views.RegisterUserView.as_view(),name='register'),
    path('rules/',views.show_rules_and_regulations,name='rules'),
    path('login/',views.LoginUser.as_view(),name='login'),
]