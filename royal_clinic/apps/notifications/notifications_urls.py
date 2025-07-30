from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('admin-notifications/', views.get_admin_notifications, name='admin-notifications'),
]