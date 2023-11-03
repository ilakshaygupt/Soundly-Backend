from django.urls import path
from . import views

urlpatterns = [
     path('api/songs/', views.SongAPI.as_view(), name='song-view'),
     path('api/songs/<int:pk>/', views.Individual.as_view(), name='song-view'),
    path('api/playlists/', views.PlaylistAPI.as_view(), name='playlist-view'),
    path('api/playlists/<int:pk>/', views.PlaylistAPI.as_view(), name='playlist-view'),
    # path('api/playlists_api/', views.Add_song_to_playlist.as_view()),
]