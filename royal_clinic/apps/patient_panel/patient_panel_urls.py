from django.urls import path
from . import views

app_name = 'patient'

urlpatterns = [
    path('patient_profile/', views.CompletePatientProfileView.as_view(), name='patient_profile'),
    path('medical_history_and_allergies/<int:id>/', views.ShowMedicalHistoryAndAllergiesView.as_view(), name='medical_history_and_allergies'),
    path('patients_list/', views.PatientsList.as_view(), name='patients_list'),
    
]