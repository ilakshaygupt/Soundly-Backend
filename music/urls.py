from django.urls import path

from . import views

urlpatterns = [
     path('api/songs/', views.SongAPI.as_view(), name='song-view'),
     path('api/songs/<int:pk>/', views.SongAPI.as_view(), name='song-view'),
    path('api/playlists/', views.PlaylistAPI.as_view(), name='playlist-view'),
    path('api/playlists/<int:pk>/', views.PlaylistAPI.as_view(), name='playlist-view'),
    path('api/playlists/<int:pk>/songs/', views.PlaylistSongAPI.as_view(), name='playlist-song-view'),#display all songs in a playlist
    path('api/playlists/<int:pk>/songs/<int:song_pk>/', views.AddSongToPlaylistAPI.as_view(), name='playlist-song-view'),#add remove a song to a playlist
    path('api/allpublicsongs/', views.AllPublicSongsAPI.as_view(), name='all-public-songs-view'),
    path('api/allpublicplaylists/', views.AllPublicPlaylistsAPI.as_view(), name='all-public-playlists-view'),
    path('api/allpublicplaylists/<int:pk>/', views.PublicSongsFromPlaylistAPI.as_view(), name='public-songs-from-playlist-view'),
    path("api/songsearch/",views.SongSearchAPI.as_view(),name="song-search-view"),
    path('api/getsong/<int:pk>/', views.GetSong.as_view(), name='get-song-view'),
    path('api/favourite/song/<int:song_id>/', views.FavouriteSongsAPI.as_view(), name='favourite-songs-view'),
    path('api/favourite/songs/', views.GetFavoriteSongsAPI.as_view(), name='favourite-songs-view'),
    path('api/favourite/playlist/<int:playlist_id>/', views.FavouritePlaylistsAPI.as_view(), name='favourite-playlists-view'),
    path('api/favourite/playlists/', views.GetFavoritePlaylistsAPI.as_view(), name='favourite-playlists-view'),

]
