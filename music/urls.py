from django.urls import path

from . import views

urlpatterns = [
    path('api/songs/', views.SongAPI.as_view(), name='song-view'),# uploader to add a song and get all songs
    path('api/songs/<int:pk>/', views.SongAPI.as_view(), name='song-view'),#  put path delete or get a single song
    path('api/playlists/', views.PlaylistAPI.as_view(), name='playlist-view'),# uploader or user to add a playlist or get all playlists
    path('api/playlists/<int:pk>/', views.PlaylistAPI.as_view(), name='playlist-view'),#  put path delete or get a single playlist by id
    path('api/playlists/<int:pk>/songs/', views.PlaylistSongAPI.as_view(), name='playlist-song-view'),#display all songs in users's playlist
    path('api/playlists/<int:pk>/songs/<int:song_pk>/', views.AddSongToPlaylistAPI.as_view(), name='playlist-song-view'),#add remove a song to a playlist
    path('api/allpublicsongs/', views.AllPublicSongsAPI.as_view(), name='all-public-songs-view'),#get all public songs
    path('api/allpublicplaylists/', views.AllPublicPlaylistsAPI.as_view(), name='all-public-playlists-view'),#get all public playlists
    path('api/allpublicplaylists/<int:pk>/', views.PublicSongsFromPlaylistAPI.as_view(), name='public-songs-from-playlist-view'),#get all public songs from a single public playlist
    path("api/songsearch/",views.SongSearchAPI.as_view(),name="song-search-view"),#search for a song
    path('api/getsong/<int:pk>/', views.GetSong.as_view(), name='get-song-view'),#get a song by id "NECESSARY FOR PLAYING SONGS"
    path('api/favourite/song/<int:song_id>/', views.FavouriteSongsAPI.as_view(), name='favourite-songs-view'),#add or remove a song from the user favourites
    path('api/favourite/songs/', views.GetFavoriteSongsAPI.as_view(), name='favourite-songs-view'),#get all user favourite songs
    path('api/favourite/playlist/<int:playlist_id>/', views.FavouritePlaylistsAPI.as_view(), name='favourite-playlists-view'),#add or remove a playlist from the user favourites
    path('api/favourite/playlists/', views.GetFavoritePlaylistsAPI.as_view(), name='favourite-playlists-view'),#get all user favourite playlists
]
