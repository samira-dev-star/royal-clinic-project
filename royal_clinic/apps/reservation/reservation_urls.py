from django.urls import path
from . import views

app_name = 'reservation'

urlpatterns = [
        # path('reserve/', views.GeneralReservationView.as_view(), name='reserve'),
        # path('get_available_times/', views.get_available_times, name='get_available_times'),
        path('reserve/', views.reservation, name='reserve'),
]