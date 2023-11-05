from django.urls import path
from . import views

urlpatterns = [
     path('api/songs/', views.SongAPI.as_view(), name='song-view'),
     path('api/songs/<int:pk>/', views.SongAPI.as_view(), name='song-view'),
    path('api/playlists/', views.PlaylistAPI.as_view(), name='playlist-view'),
    path('api/playlists/<int:pk>/', views.PlaylistAPI.as_view(), name='playlist-view'),
    path('api/playlists/<int:pk>/songs/', views.PlaylistSongAPI.as_view(), name='playlist-song-view'),#display all songs in a playlist
    path('api/playlists/<int:pk>/songs/<int:song_pk>/', views.AddSongToPlaylistAPI.as_view(), name='playlist-song-view'),#add a song to a playlist
]
