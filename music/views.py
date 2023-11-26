import re
from operator import itemgetter

import cloudinary
from django.db.models import Q
from django.shortcuts import get_object_or_404
from fuzzywuzzy import fuzz, process
from rest_framework import generics, status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from accounts.renderers import *
from music.serializers import *

from .models import *


class SongAPI(APIView):
    serializer_class = SongDisplaySerializer
    renderer_classes = [UserRenderer]
    authentication_classes = [JWTAuthentication]

    parser_classes = [MultiPartParser, FormParser]
    
    def post(self, request):
        serializer = SongCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            
            serializer.create(serializer.validated_data)

            return Response({
                'message': 'Song uploaded successfully'
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, song_id):
        uploader = request.user
        if uploader.is_uploader == False:
                return Response({'message': 'Only uploaders can add songs'}, status=status.HTTP_403_FORBIDDEN)
        try:
            song = Song.objects.get(id=song_id)
        except Song.DoesNotExist:
            return Response({'message': 'Song not found'}, status=status.HTTP_404_NOT_FOUND)
        if song.uploader != request.user:
            return Response({'message': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
        serializer = ChangeSongSerializer(
            song, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Song partially updated',
                "data": serializer.data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, song_id=None):
        uploader = request.user
        if uploader.is_uploader == False:
                return Response({'message': 'Only uploaders can add songs'}, status=status.HTTP_403_FORBIDDEN)
        if song_id is not None:
            try:
                song = Song.objects.get(id=song_id)
                if song.uploader != request.user:
                    return Response({'message': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
                serializer = SongDisplaySerializer(song)
                return Response({"data": serializer.data, "message": "found song"})
            except Song.DoesNotExist:
                return Response({'message': 'Song not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            songs = Song.objects.filter(uploader=request.user)
            public_songs = songs.filter(is_private=False)
            private_songs = songs.filter(is_private=True)
            public_songs_data = SongDisplaySerializer(public_songs, many=True)
            private_songs_data = SongDisplaySerializer(
                private_songs, many=True)
            return Response({"data": {"public songs": public_songs_data.data, "private songs": private_songs_data.data}, "message": "all songs"})

    def delete(self, request, song_id):
        uploader = request.user
        if uploader.is_uploader == False:
                return Response({'message': 'Only uploaders can add songs'}, status=status.HTTP_403_FORBIDDEN)
        try:
            song = Song.objects.get(id=song_id)
        except Song.DoesNotExist:
            return Response({'message': 'Song not found'}, status=status.HTTP_404_NOT_FOUND)
        if song.uploader != request.user:
            return Response({'message': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
        song.delete()
        return Response({'message': 'Song deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class PlaylistAPI(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PlaylistDisplaySerializer
    renderer_classes = [UserRenderer]
    authentication_classes = [JWTAuthentication]
    parser_classes = [MultiPartParser, FormParser]
    lookup_field = "playlist_id"
    def get_queryset(self):
        if self.kwargs.get("playlist_id"):
            return Playlist.objects.filter(
                id=self.kwargs.get("playlist_id"), uploader=self.request.user
            )
        else:
            return Playlist.objects.filter(uploader=self.request.user)

    def get(self, request, *args, **kwargs):
        playlist_id = kwargs.get("playlist_id")
        if playlist_id:
            return self.retrieve(request, *args, **kwargs)
        else:
            return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = PlaylistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(uploader=request.user)
            return Response(
                {
                    "status": status.HTTP_201_CREATED,
                    "message": "Playlist created successfully",
                    "data": serializer.data,
                }
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        playlist_id = kwargs.get("playlist_id")
        if playlist_id:
            return self.partial_update(request, *args, **kwargs)
        return Response(
            {"message": "Playlist ID is required for partial update"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, *args, **kwargs):
        playlist_id = kwargs.get("playlist_id")
        if playlist_id:
            return self.destroy(request, *args, **kwargs)
        return Response(
            {"message": "Playlist ID is required for deletion"},
            status=status.HTTP_400_BAD_REQUEST,
        )

class PlaylistSongAPI(generics.ListAPIView):
    renderer_classes = [UserRenderer]
    authentication_classes = [JWTAuthentication]
    serializer_class = SongDisplaySerializer

    def get_queryset(self):
        playlist_id = self.kwargs.get('playlist_id')
        try:
            playlist = Playlist.objects.get(id=playlist_id)
        except Playlist.DoesNotExist:
            return Song.objects.none()

        if playlist.uploader != self.request.user:
            return Song.objects.none()

        return playlist.songs.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({'message': 'No songs in playlist or access denied'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(queryset, many=True)
        playlist_id = kwargs.get('playlist_id')
        try:
            playlist = Playlist.objects.get(id=playlist_id)
        except Playlist.DoesNotExist:
            return Response({'message': 'Playlist not found'}, status=status.HTTP_404_NOT_FOUND)

        playlist_serializer = PlaylistDisplaySerializer(playlist)

        return Response({"data": {"playlist": playlist_serializer.data, "songs": serializer.data}, "message": "All songs displayed"}, status=status.HTTP_200_OK)

class AddSongToPlaylistAPI(generics.CreateAPIView, generics.DestroyAPIView):
    renderer_classes = [UserRenderer]
    authentication_classes = [JWTAuthentication]
    serializer_class = PlaylistSerializer  # Replace with your actual serializer

    def get_queryset(self):
        playlist_id = self.kwargs.get('playlist_id')
        return Playlist.objects.filter(id=playlist_id)

    def post(self, request, *args, **kwargs):
        playlist = self.get_object()
        song_id = kwargs.get('song_id')

        try:
            song = Song.objects.get(id=song_id)
        except Song.DoesNotExist:
            return Response({'message': 'Song not found'}, status=status.HTTP_404_NOT_FOUND)

        if playlist.uploader != request.user:
            return Response({'message': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)

        playlist.songs.add(song)
        serializer = self.get_serializer(playlist)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        playlist = self.get_object()
        song_id = kwargs.get('song_id')

        try:
            song = Song.objects.get(id=song_id)
        except Song.DoesNotExist:
            return Response({'message': 'Song not found'}, status=status.HTTP_404_NOT_FOUND)

        if playlist.uploader != request.user:
            return Response({'message': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)

        playlist.songs.remove(song)
        return Response({'message': 'Song removed from the playlist'}, status=status.HTTP_204_NO_CONTENT)


class AllPublicSongsAPI(generics.ListAPIView):
    # renderer_classes = [UserRenderer]
    authentication_classes = [JWTAuthentication]
    serializer_class = SongDisplaySerializer

    def get_queryset(self):
        return Song.objects.filter(is_private=False)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"data": serializer.data, "message": "All public songs displayed"}, status=status.HTTP_200_OK)

class AllPublicPlaylistsAPI(generics.ListAPIView):
    renderer_classes = [UserRenderer]
    authentication_classes = [JWTAuthentication]
    serializer_class = PlaylistDisplaySerializer

    def get_queryset(self):
        return Playlist.objects.filter(is_private=False)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"data": serializer.data, "message": "All public playlists displayed"}, status=status.HTTP_200_OK)

class PublicSongsFromPlaylistAPI(generics.ListAPIView):
    # renderer_classes = [UserRenderer]
    authentication_classes = [JWTAuthentication]
    serializer_class = SongDisplaySerializer

    def get_queryset(self):
        playlist_id = self.kwargs.get('playlist_id')
        try:
            playlist = Playlist.objects.get(id=playlist_id)
        except Playlist.DoesNotExist:
            return Song.objects.none()

        if playlist.is_private:
            return Song.objects.none()

        return playlist.songs.filter(is_private=False)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({'message': 'No songs in playlist or all songs are private'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(queryset, many=True)
        playlist_id = kwargs.get('playlist_id')
        try:
            playlist = Playlist.objects.get(id=playlist_id)
        except Playlist.DoesNotExist:
            return Response({'message': 'Playlist not found'}, status=status.HTTP_404_NOT_FOUND)

        playlist_serializer = PlaylistDisplaySerializer(playlist)

        return Response({"data": {"playlist": playlist_serializer.data, "songs": serializer.data}, "message": "All public songs from playlist displayed"}, status=status.HTTP_200_OK)

class SongSearchAPI(APIView):
    renderer_classes = [UserRenderer]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        query = request.GET.get('query')

        if not query:
            return Response({'message': 'No search parameters provided'}, status=status.HTTP_400_BAD_REQUEST)

        songs = Song.objects.filter(is_private=False)

        q_objects = Q()

        def fuzzy_search(field, query):
            values = Song.objects.values_list(field, flat=True)
            matches = process.extract(
                query, values, scorer=fuzz.ratio, limit=None)
            sorted_matches = sorted(matches, key=itemgetter(1), reverse=True)
            similar_values = [value for value,
                              score in sorted_matches if score > 1.8]
            return Q(**{f'{field}__in': similar_values})

        keywords = query.split()
        q_objects = Q()

        for keyword in keywords:
            q_objects |= fuzzy_search('name', keyword)
            q_objects |= fuzzy_search('artist__name', keyword)
            q_objects |= fuzzy_search('language__name', keyword)
            q_objects |= fuzzy_search('genre__name', keyword)
            q_objects |= fuzzy_search('mood__name', keyword)
            q_objects |= fuzzy_search('uploader__username', keyword)

        songs = songs.filter(q_objects).distinct()
        if not songs:
            return Response({'message': 'No songs found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = SongDisplaySerializer(
            songs, many=True, context={'user': request.user})
        return Response({"data": serializer.data, "message": "Songs matching the search criteria"}, status=status.HTTP_200_OK)


class GetSong(generics.RetrieveAPIView):
    renderer_classes = [UserRenderer]
    authentication_classes = [JWTAuthentication]
    serializer_class = SongSerializer

    def get_queryset(self):
        return Song.objects.all()

    def retrieve(self, request, *args, **kwargs):
        song_id = kwargs.get('song_id')
        queryset = self.get_queryset()

        try:
            song = queryset.get(id=song_id)
        except Song.DoesNotExist:
            return Response({'message': 'Song not found'}, status=status.HTTP_404_NOT_FOUND)

        if song.is_private and song.uploader != request.user:
            return Response({'message': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
        else:
            serializer = self.get_serializer(song, context={'user': request.user})
            try:
                recently_played = RecentlyPlayed.objects.get(
                    user=request.user, song=song)
                recently_played.save()
            except RecentlyPlayed.DoesNotExist:
                recently_played = RecentlyPlayed.objects.create(
                    user=request.user, song=song)
                recently_played.save()

            return Response({"data": serializer.data, "message": "Song found"}, status=status.HTTP_200_OK)


class RecentlyPlayedAPI(generics.ListAPIView):
    renderer_classes = [UserRenderer]
    authentication_classes = [JWTAuthentication]
    serializer_class = SongDisplaySerializer

    def get_queryset(self):
        user = self.request.user
        recently_played = RecentlyPlayed.objects.filter(user=user)
        if recently_played.count() == 0:
            return Song.objects.none()
        return Song.objects.filter(recentlyplayed__in=recently_played).order_by('-recentlyplayed__timestamp')[:6]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({'message': 'No songs found'}, status=status.HTTP_204_NO_CONTENT)
        serializer = self.get_serializer(queryset, many=True)
        return Response({"data": serializer.data, "message": "Songs found"}, status=status.HTTP_200_OK)


class FavouriteSongsAPI(generics.CreateAPIView, generics.DestroyAPIView):
    renderer_classes = [UserRenderer]
    authentication_classes = [JWTAuthentication]
    def get_favourite(self):
        user = self.request.user
        return get_object_or_404(Favourite, user=user)

    def post(self, request, *args, **kwargs):
        favourite = self.get_favourite()
        song_id = kwargs.get('song_id')
        try:
            song = Song.objects.get(id=song_id)
        except Song.DoesNotExist:
            return Response({'message': 'Song not found'}, status=status.HTTP_404_NOT_FOUND)
        favourite.song.add(song)
        return Response({"message": "Song added to favourites"}, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        favourite = self.get_favourite()
        song_id = kwargs.get('song_id')
        try:
            song = Song.objects.get(id=song_id)
        except Song.DoesNotExist:
            return Response({'message': 'Song not found'}, status=status.HTTP_404_NOT_FOUND)
        if song in favourite.song.all():
            favourite.song.remove(song)
            return Response({"message": "Song removed from favourites"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Song is not in your favorites"}, status=status.HTTP_400_BAD_REQUEST)

class GetFavoriteSongsAPI(generics.ListAPIView):
    renderer_classes = [UserRenderer]
    authentication_classes = [JWTAuthentication]
    serializer_class = SongDisplaySerializer

    def get_queryset(self):
        user = self.request.user
        favourite = get_object_or_404(Favourite, user=user)
        return favourite.song.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset.count() == 0:
            return Response({'message': 'No songs found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(queryset, many=True)
        return Response({"data": serializer.data, "message": "Songs found"}, status=status.HTTP_200_OK)

class GetFavoriteartistAPI(generics.ListAPIView, generics.CreateAPIView, generics.DestroyAPIView):
    renderer_classes = [UserRenderer]
    authentication_classes = [JWTAuthentication]
    serializer_class = artistSerializer

    def get_queryset(self):
        user = self.request.user
        favourite = get_object_or_404(Favourite, user=user)
        return favourite.artist.all()

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"data": serializer.data, "message": "Artists found"}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = AddFavArtists(data=request.data)

        if serializer.is_valid():
            artist_names = serializer.validated_data.get('artist_names', [])

            if not artist_names:
                return Response({"message": "At least one artist name is required"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                favourite = Favourite.objects.get(user=user)
            except Favourite.DoesNotExist:
                return Response({"message": "User does not have a favourite object"}, status=status.HTTP_400_BAD_REQUEST)

            for artist_name in artist_names:
                artist, created = Artist.objects.get_or_create(name=artist_name)
                if not favourite.artist.filter(name=artist_name).exists():
                    favourite.artist.add(artist)

            return Response({"message": "Artists added to favorites"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            favourite = get_object_or_404(Favourite, user=user)
            artist_name = serializer.validated_data.get('name', None)

            if artist_name is None:
                return Response({"message": "Artist name is required"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                artist = Artist.objects.get(name=artist_name)
            except Artist.DoesNotExist:
                artist = Artist.objects.create(name=artist_name)

            if artist in favourite.artist.all():
                favourite.artist.remove(artist)
                return Response({"message": "Artist removed"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Artist is not in your favorites"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AllArtistsAPI(generics.ListAPIView):
    renderer_classes = [UserRenderer]
    authentication_classes = [JWTAuthentication]
    serializer_class = artistSerializer

    def get_queryset(self):
        return Artist.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"data": serializer.data, "message": "Artists found"}, status=status.HTTP_200_OK)
class ArtistAPI(generics.RetrieveAPIView):
    renderer_classes = [UserRenderer]
    authentication_classes = [JWTAuthentication]
    queryset = Artist.objects.all()
    serializer_class = artistSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        songs = Song.objects.filter(artist=instance)
        song_serializer = SongDisplaySerializer(songs, many=True)
        return Response({"data": {"artist": serializer.data, "songs": song_serializer.data}, "message": "Artist found"}, status=status.HTTP_200_OK)

class ForYouAPI(generics.ListAPIView):
    renderer_classes = [UserRenderer]
    authentication_classes = [JWTAuthentication]
    serializer_class = SongDisplaySerializer

    def get_queryset(self):
        user = self.request.user

        try:
            favourite = Favourite.objects.get(user=user)
        except Favourite.DoesNotExist:
            favourite = None

        recently_played_songs = RecentlyPlayed.objects.filter(user=user)
        combined_songs = Song.objects.none()

        if favourite:
            characteristic_query_fav = Q()
            for song in favourite.song.all():
                characteristic_query_fav |= Q(artist=song.artist) & Q(
                    genre=song.genre) & Q(mood=song.mood)
            similar_songs_from_favs = Song.objects.filter(
                characteristic_query_fav)
            combined_songs |= similar_songs_from_favs

        characteristic_query_recent = Q()
        for recently_played in recently_played_songs:
            song = recently_played.song
            characteristic_query_recent |= Q(artist=song.artist) & Q(
                genre=song.genre) & Q(mood=song.mood)
        similar_songs_from_recent = Song.objects.filter(
            characteristic_query_recent)

        combined_songs |= similar_songs_from_recent

        if combined_songs.count() == 0:
            combined_songs = Song.objects.all()

        return combined_songs

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True, context={'user': request.user})
        return Response({"data": serializer.data, "message": "Similar songs found"}, status=status.HTTP_200_OK)
class GetFavoriteLanguageAPI(generics.ListCreateAPIView):
    renderer_classes = [UserRenderer]
    authentication_classes = [JWTAuthentication]
    serializer_class = LanguageSerializer

    def get_queryset(self):
        user = self.request.user
        favourite, created = Favourite.objects.get_or_create(user=user)
        return favourite.language.all()

    def list(self, request, *args, **kwargs):
        languages = self.get_queryset()
        serializer = self.get_serializer(languages, many=True)
        return Response({"data": serializer.data, "message": "languages found"}, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        user = request.user
        serializer = AddFavLanguages(data=request.data)

        if serializer.is_valid():
            language_names = serializer.validated_data.get('language_names', [])

            if not language_names:
                return Response({"message": "At least one language name is required"}, status=status.HTTP_400_BAD_REQUEST)

            favourite, created = Favourite.objects.get_or_create(user=user)

            for language_name in language_names:
                language, created = Language.objects.get_or_create(name=language_name)

                if not favourite.language.filter(name=language_name).exists():
                    favourite.language.add(language)

            return Response({"message": "Languages added to favorites"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
