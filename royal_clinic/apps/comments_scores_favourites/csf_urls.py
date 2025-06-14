from django.urls import path
from . import views

app_name = 'csf'

urlpatterns = [
    path("create_comment/<slug:slug>/",views.CommentView.as_view(),name="create_comment"),
    path("users_ideas/",views.ShowAllScoresAndIdeasView.as_view(),name="users_ideas"),
    path("add_score/",views.add_score,name="add_score"),
]