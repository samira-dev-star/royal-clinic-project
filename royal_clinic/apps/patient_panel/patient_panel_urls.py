from django.urls import path
from . import views

app_name = 'patient'

urlpatterns = [
    path('patient_profile/', views.CompletePatientProfileView.as_view(), name='patient_profile'),
]