import os
import re
from operator import itemgetter

import cloudinary
from django.db.models import Q
from django.shortcuts import get_object_or_404
from fuzzywuzzy import fuzz, process
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from accounts.renderers import *
from music.serializers import *
from .models import *

ALLOWED_AUDIO_EXTENSIONS = [
    ".mp3",
    ".wav",
    ".acc",
    ".flac",
    ".wma",
    ".aiff",
    ".pcm",
    ".m4a",
]
ALLOWED_THUMBNAIL_EXTENSIONS = [".png", ".jpeg", ".jpg", ".webp", ".avif", ".svg"]


class SongAPI(APIView):
    serializer_class = SongDisplaySerializer
    renderer_classes = [UserRenderer]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = SongCreateSerializer(data=request.data)
        if serializer.is_valid():
            uploader = request.user
            lyrics_url = None
            if uploader.is_uploader == False:
                return Response(
                    {"message": "Only uploaders can add songs"},
                    status=status.HTTP_403_FORBIDDEN,
                )
            audio_url = None
            if "audio" in request.FILES:
                if request.FILES["audio"].size > 7000000:
                    return Response(
                        {"message": "Audio file size must be less than 7MB"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                _, audio_extension = os.path.splitext(request.FILES["audio"].name)
                if audio_extension.lower() not in ALLOWED_AUDIO_EXTENSIONS:
                    return Response(
                        {
                            "message": "Invalid audio file type. Supported types: mp3, wav, acc, flac, wma, aiff, pcm, m4a"
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            else:
                return Response(
                    {"message": "Audio file is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            thumbnail_url = None
            if "thumbnail" in request.FILES:
                if request.FILES["thumbnail"].size > 4000000:
                    return Response(
                        {"message": "Thumbnail file size must be less than 4MB"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                _, thumbnail_extension = os.path.splitext(
                    request.FILES["thumbnail"].name
                )
                if thumbnail_extension.lower() not in ALLOWED_THUMBNAIL_EXTENSIONS:
                    return Response(
                        {
                            "message": "Invalid thumbnail file type. Supported types: png, jpeg, jpg, webp, avif, svg"
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            else:
                return Response(
                    {"message": "Thumbnail is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if "lyrics" in request.FILES:
                if request.FILES["lyrics"].size > 4000000:
                    return Response(
                        {"message": "Lyrics file size must be less than 4MB"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                if not re.search(
                    r"\.srt$", request.FILES["lyrics"].name, re.IGNORECASE
                ):
                    return Response(
                        {"message": "Lyrics file type must be srt"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                lyrics = request.FILES["lyrics"]
                lyrics_response = cloudinary.uploader.upload(
                    lyrics, secure=True, resource_type="raw"
                )
                lyrics_url = lyrics_response.get("url")
            else:
                lyrics_url = None

            thumbnail = request.FILES["thumbnail"]
            thumbnail_response = cloudinary.uploader.upload(thumbnail, secure=True)
            thumbnail_url = thumbnail_response.get("url")
            audio = request.FILES["audio"]
            audio_response = cloudinary.uploader.upload(
                audio, secure=True, resource_type="video"
            )
            audio_url = audio_response.get("url")

            language_name = serializer.validated_data.pop("language_name", None)
            mood_name = serializer.validated_data.pop("mood_name", None)
            genre_name = serializer.validated_data.pop("genre_name", None)
            artist_name = serializer.validated_data.pop("artist_name", None)
            try:
                language = Language.objects.get(name=language_name)
            except Language.DoesNotExist:
                language = Language.objects.create(name=language_name)
            try:
                artist = Artist.objects.get(name=artist_name)
            except Artist.DoesNotExist:
                artist = Artist.objects.create(name=artist_name)
            try:
                mood = Mood.objects.get(name=mood_name)
            except Mood.DoesNotExist:
                mood = Mood.objects.create(name=mood_name)
            try:
                genre = Genre.objects.get(name=genre_name)
            except Genre.DoesNotExist:
                genre = Genre.objects.create(name=genre_name)
            if audio_url is None:
                lyrics_json = None
            song = Song.objects.create(
                uploader=uploader,
                thumbnail_url=thumbnail_url,
                song_url=audio_url,
                language=language,
                mood=mood,
                genre=genre,
                artist=artist,
                lyrics_url=lyrics_url,
                **serializer.validated_data,
            )
            songe = Song.objects.get(id=song.id)
            songe.download_lyrics_and_save_json()
            songe.save()

            return Response(
                {"message": "Song uploaded successfully"},
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, song_id):
        uploader = request.user
        if uploader.is_uploader == False:
            return Response(
                {"message": "Only uploaders can add songs"},
                status=status.HTTP_403_FORBIDDEN,
            )
        try:
            song = Song.objects.get(id=song_id)
        except Song.DoesNotExist:
            return Response(
                {"message": "Song not found"}, status=status.HTTP_404_NOT_FOUND
            )
        if song.uploader != request.user:
            return Response(
                {"message": "Access denied"}, status=status.HTTP_403_FORBIDDEN
            )
        serializer = ChangeSongSerializer(song, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Song partially updated", "data": serializer.data}
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, song_id=None):
        uploader = request.user
        if uploader.is_uploader == False:
            return Response(
                {"message": "Only uploaders can add songs"},
                status=status.HTTP_403_FORBIDDEN,
            )
        if song_id is not None:
            try:
                song = Song.objects.get(id=song_id)
                if song.uploader != request.user:
                    return Response(
                        {"message": "Access denied"}, status=status.HTTP_403_FORBIDDEN
                    )
                serializer = SongDisplaySerializer(song)
                return Response({"data": serializer.data, "message": "found song"})
            except Song.DoesNotExist:
                return Response(
                    {"message": "Song not found"}, status=status.HTTP_404_NOT_FOUND
                )
        else:
            songs = Song.objects.filter(uploader=request.user)
            public_songs = songs.filter(is_private=False)
            private_songs = songs.filter(is_private=True)
            public_songs_data = SongDisplaySerializer(public_songs, many=True)
            private_songs_data = SongDisplaySerializer(private_songs, many=True)
            return Response(
                {
                    "data": {
                        "public songs": public_songs_data.data,
                        "private songs": private_songs_data.data,
                    },
                    "message": "all songs",
                }
            )

    def delete(self, request, song_id):
        uploader = request.user
        if uploader.is_uploader == False:
            return Response(
                {"message": "Only uploaders can add songs"},
                status=status.HTTP_403_FORBIDDEN,
            )
        try:
            song = Song.objects.get(id=song_id)
        except Song.DoesNotExist:
            return Response(
                {"message": "Song not found"}, status=status.HTTP_404_NOT_FOUND
            )
        if song.uploader != request.user:
            return Response(
                {"message": "Access denied"}, status=status.HTTP_403_FORBIDDEN
            )
        song.delete()
        return Response(
            {"message": "Song deleted successfully"}, status=status.HTTP_204_NO_CONTENT
        )


class PlaylistAPI(APIView):
    serializer_class = PlaylistSerializer
    renderer_classes = [UserRenderer]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            uploader = request.user
            serializer.save(uploader=uploader)
            return Response(
                {
                    "status": status.HTTP_201_CREATED,
                    "message": "Playlist created successfully",
                    "data": serializer.data,
                }
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, playlist_id=None):
        if playlist_id:
            try:
                playlist = Playlist.objects.get(id=playlist_id)
                if playlist.uploader == request.user:
                    serializer = PlaylistDisplaySerializer(playlist)
                    return Response(
                        {"data": serializer.data, "message": "found playlist"}
                    )
                else:
                    return Response(
                        {"message": "Access denied"}, status=status.HTTP_403_FORBIDDEN
                    )
            except Playlist.DoesNotExist:
                return Response(
                    {"message": "Playlist not found"}, status=status.HTTP_404_NOT_FOUND
                )
        else:
            try:
                playlists = Playlist.objects.filter(uploader=request.user)
            except Playlist.DoesNotExist:
                return Response(
                    {"message": "Playlist not found"}, status=status.HTTP_404_NOT_FOUND
                )
            serializer = PlaylistDisplaySerializer(playlists, many=True)
            return Response({"data": serializer.data, "message": "all user playlist"})

    def patch(self, request, playlist_id):
        try:
            playlist = Playlist.objects.get(id=playlist_id)
        except Playlist.DoesNotExist:
            return Response(
                {"message": "Playlist not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = ChangePlaylistSerializer(playlist, data=request.data, partial=True)
        if serializer.is_valid():
            if playlist.uploader != request.user:
                return Response(
                    {"message": "Access denied"}, status=status.HTTP_403_FORBIDDEN
                )
            serializer.save()
            return Response(
                {"message": "Playlist partially updated", "data": serializer.data}
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, playlist_id):
        try:
            playlist = Playlist.objects.get(id=playlist_id)
        except Playlist.DoesNotExist:
            return Response(
                {"message": "Playlist not found"}, status=status.HTTP_404_NOT_FOUND
            )
        if playlist.uploader != request.user:
            return Response(
                {"message": "Access denied"}, status=status.HTTP_403_FORBIDDEN
            )
        playlist.delete()
        return Response(
            {"message": "Playlist deleted"}, status=status.HTTP_204_NO_CONTENT
        )


class PlaylistSongAPI(APIView):
    renderer_classes = [UserRenderer]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, playlist_id):
        try:
            playlist = Playlist.objects.get(id=playlist_id)
        except Playlist.DoesNotExist:
            return Response(
                {"message": "Playlist not found"}, status=status.HTTP_404_NOT_FOUND
            )
        if playlist.uploader != request.user:
            return Response(
                {"message": "Access denied"}, status=status.HTTP_403_FORBIDDEN
            )
        songs = playlist.songs.all()
        serializer = SongDisplaySerializer(songs, many=True)
        playlist_serializer = PlaylistDisplaySerializer(playlist)

        return Response(
            {
                "data": {
                    "playlist": playlist_serializer.data,
                    "songs": serializer.data,
                },
                "message": "all songs displayed",
            },
            status=status.HTTP_200_OK,
        )


class AddSongToPlaylistAPI(APIView):
    renderer_classes = [UserRenderer]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, playlist_id, song_id):
        try:
            playlist = Playlist.objects.get(id=playlist_id)
        except Playlist.DoesNotExist:
            return Response(
                {"message": "Playlist not found"}, status=status.HTTP_404_NOT_FOUND
            )
        try:
            song = Song.objects.get(id=song_id)
        except Song.DoesNotExist:
            return Response(
                {"message": "Song not found"}, status=status.HTTP_404_NOT_FOUND
            )
        if playlist.uploader != request.user:
            return Response(
                {"message": "Access denied"}, status=status.HTTP_403_FORBIDDEN
            )
        playlist.songs.add(song)
        return Response(
            {"message": "Song added successfully to the playlist"},
            status=status.HTTP_201_CREATED,
        )

    def delete(self, request, playlist_id, song_id):
        try:
            playlist = Playlist.objects.get(id=playlist_id)
        except Playlist.DoesNotExist:
            return Response(
                {"message": "Playlist not found"}, status=status.HTTP_404_NOT_FOUND
            )

        try:
            song = Song.objects.get(id=song_id)
        except Song.DoesNotExist:
            return Response(
                {"message": "Song not found"}, status=status.HTTP_404_NOT_FOUND
            )
        if playlist.uploader != request.user:
            return Response(
                {"message": "Access denied"}, status=status.HTTP_403_FORBIDDEN
            )
        playlist.songs.remove(song)
        return Response(
            {"message": "Song removed from the playlist"},
            status=status.HTTP_204_NO_CONTENT,
        )


class AllPublicSongsAPI(APIView):
    renderer_classes = [UserRenderer]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        songs = Song.objects.filter(is_private=False)
        serializer = SongDisplaySerializer(
            songs, many=True, context={"user": request.user}
        )
        return Response(
            {"data": serializer.data, "message": "all public songs displayed"},
            status=status.HTTP_200_OK,
        )


class AllPublicPlaylistsAPI(APIView):
    renderer_classes = [UserRenderer]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        playlists = Playlist.objects.filter(is_private=False)
        serializer = PlaylistDisplaySerializer(
            playlists, many=True, context={"user": request.user}
        )
        return Response(
            {"data": serializer.data, "message": "all public playlists displayed"},
            status=status.HTTP_200_OK,
        )


class PublicSongsFromPlaylistAPI(APIView):
    renderer_classes = [UserRenderer]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, playlist_id):
        try:
            playlist = Playlist.objects.get(id=playlist_id)
        except Playlist.DoesNotExist:
            return Response(
                {"message": "Playlist not found"}, status=status.HTTP_404_NOT_FOUND
            )
        if playlist.is_private:
            return Response(
                {"message": "Access denied"}, status=status.HTTP_403_FORBIDDEN
            )
        if playlist.songs.count() == 0:
            return Response(
                {"message": "No songs in playlist"}, status=status.HTTP_404_NOT_FOUND
            )
        songs = playlist.songs.filter(is_private=False)
        serializer = SongDisplaySerializer(
            songs, many=True, context={"user": request.user}
        )
        playlist_serializer = PlaylistDisplaySerializer(playlist)

        return Response(
            {
                "data": {
                    "playlist": playlist_serializer.data,
                    "songs": serializer.data,
                },
                "message": "all public songs from playlist displayed",
            },
            status=status.HTTP_200_OK,
        )


class SongSearchAPI(APIView):
    renderer_classes = [UserRenderer]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = request.GET.get("query")

        if not query:
            return Response(
                {"message": "No search parameters provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        songs = Song.objects.filter(is_private=False)

        q_objects = Q()

        def fuzzy_search(field, query):
            values = Song.objects.values_list(field, flat=True)
            matches = process.extract(query, values, scorer=fuzz.ratio, limit=None)
            sorted_matches = sorted(matches, key=itemgetter(1), reverse=True)
            similar_values = [value for value, score in sorted_matches if score > 61.8]
            return Q(**{f"{field}__in": similar_values})

        keywords = query.split()
        q_objects = Q()

        for keyword in keywords:
            q_objects |= fuzzy_search("name", keyword)
            q_objects |= fuzzy_search("artist__name", keyword)
            q_objects |= fuzzy_search("language__name", keyword)
            q_objects |= fuzzy_search("genre__name", keyword)
            q_objects |= fuzzy_search("mood__name", keyword)
            q_objects |= fuzzy_search("uploader__username", keyword)

        songs = songs.filter(q_objects).distinct()
        if not songs:
            return Response(
                {"message": "No songs found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = SongDisplaySerializer(
            songs, many=True, context={"user": request.user}
        )
        return Response(
            {"data": serializer.data, "message": "Songs matching the search criteria"},
            status=status.HTTP_200_OK,
        )


class GetSong(APIView):
    renderer_classes = [UserRenderer]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, song_id):
        try:
            song = Song.objects.get(id=song_id)
        except Song.DoesNotExist:
            return Response(
                {"message": "Song not found"}, status=status.HTTP_404_NOT_FOUND
            )

        if song.is_private and song.uploader != request.user:
            return Response(
                {"message": "Access denied"}, status=status.HTTP_403_FORBIDDEN
            )
        else:
            serializer = SongSerializer(song, context={"user": request.user})
            try:
                recently_played = RecentlyPlayed.objects.get(
                    user=request.user, song=song
                )
                recently_played.save()
            except RecentlyPlayed.DoesNotExist:
                recently_played = RecentlyPlayed.objects.create(
                    user=request.user, song=song
                )
                recently_played.save()

            return Response(
                {"data": serializer.data, "message": "Song found"},
                status=status.HTTP_200_OK,
            )


class RecentlyPlayedAPI(APIView):
    renderer_classes = [UserRenderer]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            recently_played = RecentlyPlayed.objects.filter(user=request.user)
            if recently_played.count() == 0:
                return Response(
                    {"message": "No songs found"}, status=status.HTTP_204_NO_CONTENT
                )
        except RecentlyPlayed.DoesNotExist:
            return Response(
                {"message": "No songs found"}, status=status.HTTP_204_NO_CONTENT
            )
        song_ids = recently_played.values_list("song__id", flat=True)
        songs = Song.objects.filter(id__in=song_ids).order_by(
            "-recentlyplayed__timestamp"
        )
        serializer = SongDisplaySerializer(
            songs, many=True, context={"user": request.user}
        )
        return Response(
            {"data": serializer.data, "message": "Songs found"},
            status=status.HTTP_200_OK,
        )


class FavouriteSongsAPI(APIView):
    renderer_classes = [UserRenderer]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, song_id):
        favourite = Favourite.objects.get(user=request.user)
        try:
            song = Song.objects.get(id=song_id)
        except Song.DoesNotExist:
            return Response(
                {"message": "Song not found"}, status=status.HTTP_404_NOT_FOUND
            )
        favourite.song.add(song)
        return Response(
            {"message": "Song added to favourites"}, status=status.HTTP_200_OK
        )

    def delete(self, request, song_id):
        favourite = Favourite.objects.get(user=request.user)
        try:
            song = Song.objects.get(id=song_id)
        except Song.DoesNotExist:
            return Response(
                {"message": "Song not found"}, status=status.HTTP_404_NOT_FOUND
            )
        if song in favourite.song.all():
            favourite.song.remove(song)
            return Response(
                {"message": "Song removed from favourites"}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"message": "Song is not in your favorites"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class GetFavoriteSongsAPI(APIView):
    renderer_classes = [UserRenderer]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        favourite = Favourite.objects.get(user=request.user)
        songs = favourite.song.all()
        if songs.count() == 0:
            return Response(
                {"message": "No songs found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = SongDisplaySerializer(
            songs, many=True, context={"user": request.user}
        )
        return Response(
            {"data": serializer.data, "message": "Songs found"},
            status=status.HTTP_200_OK,
        )


class GetFavoriteartistAPI(APIView):
    renderer_classes = [UserRenderer]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        favourite = get_object_or_404(Favourite, user=user)
        artists = favourite.artist.all()
        serializer = artistSerializer(artists, many=True)
        return Response(
            {"data": serializer.data, "message": "artists found"},
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        user = request.user
        serializer = AddFavArtists(data=request.data)

        if serializer.is_valid():
            artist_names = serializer.validated_data.get("artist_names", [])

            if not artist_names:
                return Response(
                    {"message": "At least one artist name is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            try:
                favourite = Favourite.objects.get(user=user)
            except Favourite.DoesNotExist:
                return Response(
                    {"message": "User does not have a favourite object"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            for artist_name in artist_names:
                try:
                    artist = Artist.objects.get(name=artist_name)
                except Artist.DoesNotExist:
                    artist = Artist.objects.create(name=artist_name)

                if not favourite.artist.filter(name=artist_name).exists():
                    favourite.artist.add(artist)

            return Response(
                {"message": "Artists added to favorites"}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user = request.user
        serializers = artistSerializer(data=request.data)
        if serializers.is_valid():
            favourite = Favourite.objects.get(user=user)
            artist = serializers.validated_data.pop("name", None)
            if artist == None:
                return Response(
                    {"message": "artist name is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            try:
                artist = Artist.objects.get(name=artist)
            except Artist.DoesNotExist:
                artist = Artist.objects.create(name=artist)
            if artist in favourite.artist.all():
                favourite.artist.remove(artist)
                return Response(
                    {"message": "artist removed"}, status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"message": "artist is not in your favorites"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class AllArtistsAPI(APIView):
    renderer_classes = [UserRenderer]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        artists = Artist.objects.all()
        serializer = artistSerializer(artists, many=True)
        return Response(
            {"data": serializer.data, "message": "artists found"},
            status=status.HTTP_200_OK,
        )


class ArtistAPI(APIView):
    renderer_classes = [UserRenderer]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, artist_id):
        try:
            artist = Artist.objects.get(id=artist_id)
        except Artist.DoesNotExist:
            return Response(
                {"message": "Artist not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = artistSerializer(artist)
        songs = Song.objects.filter(artist=artist)
        song_serializer = SongDisplaySerializer(songs, many=True)
        return Response(
            {
                "data": {"artist": serializer.data, "songs": song_serializer.data},
                "message": "artist found",
            },
            status=status.HTTP_200_OK,
        )


class ForYouAPI(APIView):
    renderer_classes = [UserRenderer]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        try:
            favourite = Favourite.objects.get(user=user)
        except Favourite.DoesNotExist:
            favourite = []
        recently_played_songs = RecentlyPlayed.objects.filter(user=user)
        combined_songs = Song.objects.none()
        characteristic_query_fav = Q()
        for song in favourite.song.all():
            characteristic_query_fav |= (
                Q(artist=song.artist) & Q(genre=song.genre) & Q(mood=song.mood)
            )
        similar_songs_from_favs = Song.objects.filter(characteristic_query_fav)

        combined_songs |= similar_songs_from_favs
        characteristic_query_recent = Q()
        for recently_played in recently_played_songs:
            song = recently_played.song
            characteristic_query_recent |= (
                Q(artist=song.artist) & Q(genre=song.genre) & Q(mood=song.mood)
            )
        similar_songs_from_recent = Song.objects.filter(characteristic_query_recent)

        combined_songs |= similar_songs_from_recent
        if combined_songs.count() == 0:
            combined_songs = Song.objects.all()
        serializer = SongDisplaySerializer(
            combined_songs, many=True, context={"user": user}
        )
        return Response(
            {"data": serializer.data, "message": "Similar songs found"},
            status=status.HTTP_200_OK,
        )


class GetFavoriteLanguageAPI(APIView):
    renderer_classes = [UserRenderer]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        favourite = Favourite.objects.get(user=user)
        languages = favourite.language.all()
        serializer = LanguageSerializer(languages, many=True)
        return Response(
            {"data": serializer.data, "message": "languages found"},
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        user = request.user
        serializer = AddFavLanguages(data=request.data)

        if serializer.is_valid():
            language_names = serializer.validated_data.get("language_names", [])

            if not language_names:
                return Response(
                    {"message": "At least one language name is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            try:
                favourite = Favourite.objects.get(user=user)
            except Favourite.DoesNotExist:
                return Response(
                    {"message": "User does not have a favourite "},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            for language_name in language_names:
                try:
                    language = Language.objects.get(name=language_name)
                except Language.DoesNotExist:
                    language = Language.objects.create(name=language_name)

                if not favourite.language.filter(name=language_name).exists():
                    favourite.language.add(language)

            return Response(
                {"message": "Languages added to favorites"}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MixedFavArtistSongs(APIView):
    renderer_classes = [UserRenderer]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            favourite = Favourite.objects.get(user=request.user)
            artists = favourite.artist.all()
            songs = Song.objects.none()
            for artist in artists:
                songs |= Song.objects.filter(artist=artist)
            serializer = SongDisplaySerializer(songs, many=True)
            return Response(
                {"data": serializer.data, "message": "Songs found"},
                status=status.HTTP_200_OK,
            )

        except Favourite.DoesNotExist:
            return Response(
                {"message": "User does not have a favorite object"},
                status=status.HTTP_404_NOT_FOUND,
            )
