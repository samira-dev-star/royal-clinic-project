from django.urls import path
from . import views

app_name = 'error_handlers'

urlpatterns = [
    path('404/',views.error_404,name='error_404'),
    # path('500/',views.error_500,name='error_500'),
]