from django.urls import path
from . import views

app_name = 'gallery'

urlpatterns = [
    path('videos/',views.video_list,name='videos'),
    path('videos_all/',views.video_list_all,name='videos_all'),
    path('video/<slug:slug>/',views.specific_video,name='video'),
]