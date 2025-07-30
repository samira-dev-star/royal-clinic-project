from django.urls import path
from . import views

app_name = 'reservation'

urlpatterns = [
        # path('reserve/', views.GeneralReservationView.as_view(), name='reserve'),
        path('reservation_main_page/', views.AppointmentReservationView.as_view(), name='reservation_main_page'),
        path('reserve/', views.reservation_partial_view, name='reserve'),
]