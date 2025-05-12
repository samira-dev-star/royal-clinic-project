from django.urls import path
from . import views

app_name = 'contacts'

urlpatterns = [
    path('show_contacts/', views.show_contacts, name='show_contacts'),
#     path('show_working_time1/',views.show_working_times1,name='show_working_time1'),
#     path('show_working_time2/',views.show_working_times2,name='show_working_time2'),
]