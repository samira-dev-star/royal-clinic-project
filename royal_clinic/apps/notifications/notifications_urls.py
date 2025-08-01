from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('get-admin-notifications/', views.get_admin_notifications, name='get-admin-notifications'),
]