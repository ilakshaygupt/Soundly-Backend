from django.urls import path

from . import views

urlpatterns = [
    # uploader to add a song and get all songs
    path('api/songs/', views.SongAPI.as_view(), name='song-view'),
    path('api/songs/<int:song_id>/', views.SongAPI.as_view(),
         name='song-view'),  # put path delete or get a single song
    # uploader or user to add a playlist or get all playlists
    path('api/playlists/', views.PlaylistAPI.as_view(), name='playlist-view'),
    path('api/playlists/<int:playlist_id>/', views.PlaylistAPI.as_view(),
         name='playlist-view'),  # put path delete or get a single playlist by id
    path('api/playlists/<int:playlist_id>/songs/', views.PlaylistSongAPI.as_view(),
         name='playlist-song-view'),  # display all songs in users's playlist
    path('api/playlists/<int:playlist_id>/songs/<int:song_id>/', views.AddSongToPlaylistAPI.as_view(),
         name='playlist-song-view'),  # add remove a song to a playlist
    path('api/allpublicsongs/', views.AllPublicSongsAPI.as_view(),
         name='all-public-songs-view'),  # get all public songs
    path('api/allpublicplaylists/', views.AllPublicPlaylistsAPI.as_view(),
         name='all-public-playlists-view'),  # get all public playlists
    path('api/allpublicplaylists/<int:playlist_id>/', views.PublicSongsFromPlaylistAPI.as_view() ,
         name='public-songs-from-playlist-view'),  # get all public songs from a single public playlist
    path("api/songsearch/", views.SongSearchAPI.as_view(),
         name="song-search-view"),  # search for a song
    # get a song by id "NECESSARY FOR PLAYING SONGS"
    path('api/getsong/<int:song_id>/', views.GetSong.as_view(), name='get-song-view'),
    path('api/favourite/song/<int:song_id>/', views.FavouriteSongsAPI.as_view(),
         name='favourite-songs-view'),  # add or remove a song from the user favourites
    path('api/favourite/songs/', views.GetFavoriteSongsAPI.as_view(),
         name='favourite-songs-view'),  # get all user favourite songs
    path('api/favourite/artist/', views.GetFavoriteartistAPI.as_view(),
         name='favourite-artist-view'),  # get  and add all user favourite artist,
     path('api/upadatedurationfromurl/', views.UpdateDurationFromUrl.as_view()),
     path('api/recentlyplayed/', views.RecentlyPlayedAPI.as_view(), name='recently-played-view'),
     path('api/allartists/', views.AllArtistsAPI.as_view(), name='all-artists-view'),
     path('api/artist/<int:artist_id>/', views.ArtistAPI.as_view(), name='artist-view'),
     path('api/foryou/', views.ForYouAPI.as_view(), name='for-you-view'),
     # paht('api')
]
