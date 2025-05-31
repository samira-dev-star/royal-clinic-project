from django.urls import path
from . import views

app_name = 'offers'

urlpatterns = [
    path('discount_partials/', views.offers_partials, name='discount_partials'),
]