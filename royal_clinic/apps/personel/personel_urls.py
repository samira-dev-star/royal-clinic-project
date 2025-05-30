from django.urls import path
from . import views

app_name = 'personel'

urlpatterns = [
    path('personel/',views.personels,name='personel'),
    path('personels/',views.ShowPersonel.as_view(),name='personels'),
]