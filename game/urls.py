from django.urls import path

from . import views

urlpatterns = [
    path('music-clips/', views.GameList.as_view(), name='music-clip-list'),#
    path('music-clips/<int:pk>/check/', views.CheckAnswer.as_view(), name='music-clip-edit'),
    path("scores/", views.ScoreList.as_view(), name="score-list"),
]
