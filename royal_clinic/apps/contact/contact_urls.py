from django.urls import path
from . import views

app_name = 'contact'

urlpatterns = [
    path('show_contacts/', views.show_contacts, name='show_contacts'),
#     path('show_working_time1/',views.show_working_times1,name='show_working_time1'),
    path('show_working_time2/',views.show_working_times2,name='show_working_time2'),
    path('user_public_message/',views.public_user_messages,name='user_public_message')
]