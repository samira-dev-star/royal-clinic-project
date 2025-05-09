from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    path('show_all_active_services/',views.ShowServices,name='show_all_active_services'),
    path('service_detail/<str:slug>/',views.ShowSpecificServiceDetailsView.as_view(),name='service_detail'),
    path('service_feature_values/<str:slug>/',views.show_service_features,name='service_feature_values'),
    path('service_advantages/<str:slug>/',views.show_service_advantages,name='service_advantages'),
    path('service_conditions/<str:slug>/',views.show_service_conditions,name='service_conditions'),
    path('service_procedures/<str:slug>/',views.show_service_procedures,name='service_procedures'),
]