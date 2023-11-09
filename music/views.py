
import cloudinary
from django.db.models import Q
from rest_framework import status
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
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = SongCreateSerializer(data=request.data)
        if serializer.is_valid():
            artist = request.user
            if artist.is_artist == False:
                return Response({'message': 'Only artists can add songs'}, status=status.HTTP_403_FORBIDDEN)
            audio_url = None
            if 'audio' in request.FILES:
                if request.FILES['audio'].size > 7000000:
                    return Response({'message': 'Audio file size must be less than 7MB'}, status=status.HTTP_400_BAD_REQUEST)
                if request.FILES['audio'].content_type != 'audio/mpeg':
                    return Response({'message': 'Audio file type must be mp3'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': 'Audio file is required'}, status=status.HTTP_400_BAD_REQUEST)
            thumbnail_url = None
            if 'thumbnail' in request.FILES:
                if request.FILES['thumbnail'].size > 4000000:
                    return Response({'message': 'Thumbnail file size must be less than 4MB'}, status=status.HTTP_400_BAD_REQUEST)
                if request.FILES['thumbnail'].content_type != 'image/png' and request.FILES['thumbnail'].content_type != 'image/jpeg':
                    return Response({'message': 'Thumbnail file type must be png or jpeg'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': 'Thumbnail is required'}, status=status.HTTP_400_BAD_REQUEST)

            thumbnail = request.FILES['thumbnail']
            thumbnail_response = cloudinary.uploader.upload(thumbnail, secure=True)
            thumbnail_url = thumbnail_response.get('url')
            audio = request.FILES['audio']
            audio_response = cloudinary.uploader.upload(audio, secure=True, resource_type='video')
            audio_url = audio_response.get('url')
            language_name = serializer.validated_data.pop('language_name', None)
            mood_name = serializer.validated_data.pop('mood_name', None)
            genre_name = serializer.validated_data.pop('genre_name', None)

            try:
                language = Language.objects.get(name=language_name)
            except Language.DoesNotExist:
                language = Language.objects.create(name=language_name)

            try:
                mood = Mood.objects.get(name=mood_name)
            except Mood.DoesNotExist:
                mood = Mood.objects.create(name=mood_name)

            try:
                genre = Genre.objects.get(name=genre_name)
            except Genre.DoesNotExist:
                genre = Genre.objects.create(name=genre_name)

            Song.objects.create(
                artist=artist,
                thumbnail_url=thumbnail_url,
                song_url=audio_url,
                language=language,
                mood=mood,
                genre=genre,
                **serializer.validated_data
            )

            return Response({
                'message': 'Song added successfully to the playlist'
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk=None):
        if pk is not None:
            try:
                song = Song.objects.get(id=pk)
                if song.artist != request.user:
                    return Response({'message': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
                serializer = SongDisplaySerializer(song)
                return Response({"data":serializer.data,"message": "found song"})
            except Song.DoesNotExist:
                return Response({'message': 'Song not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            songs = Song.objects.filter(artist=request.user)
            serializer = SongDisplaySerializer(songs, many=True)
            return Response({"data":serializer.data,"message": "all songs"})

    def patch(self, request, pk ):
        try:
            song = Song.objects.get(id=pk)
        except Song.DoesNotExist:
            return Response({'message': 'Song not found'}, status=status.HTTP_404_NOT_FOUND)
        if song.artist != request.user:
            return Response({'message': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
        serializer = ChangeSongSerializer(song, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Song partially updated',
                "data": serializer.data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            song = Song.objects.get(id=pk)
        except Song.DoesNotExist:
            return Response({'message': 'Song not found'}, status=status.HTTP_404_NOT_FOUND)
        if song.artist != request.user:
            return Response({'message': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
        song.delete()
        return Response({'message': 'Song deleted successfully'}, status=status.HTTP_204_NO_CONTENT)




class PlaylistAPI(APIView):
    serializer_class = PlaylistSerializer
    renderer_classes = [UserRenderer]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            artist = request.user
            thumbnail_url = None
            if 'thumbnail' in request.FILES:
                thumbnail = request.FILES['thumbnail']
                thumbnail_response = cloudinary.uploader.upload(thumbnail,secure=True,)
                thumbnail_url = thumbnail_response.get('url')
            serializer.save(artist=artist,thumbnail_url=thumbnail_url)
            return Response({
                "status" : status.HTTP_201_CREATED,
                'message': 'Playlist created successfully'
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def get(self, request, pk=None):
        if pk:
            try:
                playlist = Playlist.objects.get(id=pk)
                if playlist.artist == request.user:
                    serializer = PlaylistDisplaySerializer(playlist)
                    return Response({"data": serializer.data, "message": "found playlist"})
                else:
                    return Response({'message': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
            except Playlist.DoesNotExist:
                return Response({'message': 'Playlist not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            try:
                playlists = Playlist.objects.filter(artist=request.user)
            except Playlist.DoesNotExist:
                return Response({'message': 'Playlist not found'}, status=status.HTTP_404_NOT_FOUND)
            serializer = PlaylistDisplaySerializer(playlists, many=True)
            return Response({"data" :serializer.data,"message": "all user playlist"})

    def patch(self, request, pk):
        try:
            playlist = Playlist.objects.get(pk=pk)
        except Playlist.DoesNotExist:
            return Response({'message': 'Playlist not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ChangePlaylistSerializer(playlist, data=request.data, partial=True)
        if serializer.is_valid():
            if playlist.artist != request.user:
                return Response({'message': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
            serializer.save()
            return Response({
                'message': 'Playlist partially updated',
                "data": serializer.data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            playlist = Playlist.objects.get(pk=pk)
        except Playlist.DoesNotExist:
            return Response({'message': 'Playlist not found'}, status=status.HTTP_404_NOT_FOUND)
        if playlist.artist != request.user:
            return Response({'message': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
        playlist.delete()
        return Response({'message': 'Playlist deleted'}, status=status.HTTP_204_NO_CONTENT)

class PlaylistSongAPI(APIView): #display all songs from a playlist
    renderer_classes = [UserRenderer]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            playlist = Playlist.objects.get(pk=pk)
        except Playlist.DoesNotExist:
            return Response({'message': 'Playlist not found'}, status=status.HTTP_404_NOT_FOUND)
        if playlist.artist != request.user:
            return Response({'message': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
        songs = playlist.songs.all()
        serializer = SongDisplaySerializer(songs, many=True)

        return Response({"data":serializer.data,"message":"all songs displayed"}, status=status.HTTP_200_OK)



class AddSongToPlaylistAPI(APIView):
    renderer_classes = [UserRenderer]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, pk,song_pk):
        try:
            playlist = Playlist.objects.get(pk=pk)
        except Playlist.DoesNotExist:
            return Response({'message': 'Playlist not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            song = Song.objects.get(id=song_pk)
        except Song.DoesNotExist:
            return Response({'message': 'Song not found'}, status=status.HTTP_404_NOT_FOUND)
        if playlist.artist != request.user and song.artist != request.user:
            return Response({'message': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
        playlist.songs.add(song)
        return Response({'message': 'Song added successfully to the playlist'}, status=status.HTTP_201_CREATED)

    def delete(self, request, pk,song_pk):
        try:
            playlist = Playlist.objects.get(pk=pk)
        except Playlist.DoesNotExist:
            return Response({'message': 'Playlist not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            song = Song.objects.get(id=song_pk)
        except Song.DoesNotExist:
            return Response({'message': 'Song not found'}, status=status.HTTP_404_NOT_FOUND)
        if playlist.artist != request.user and song.artist != request.user:
            return Response({'message': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
        playlist.songs.remove(song)
        return Response({'message': 'Song removed from the playlist'}, status=status.HTTP_204_NO_CONTENT)




class AllPublicSongsAPI(APIView):
    renderer_classes = [UserRenderer]


    def get(self,format=None):
        songs = Song.objects.filter(is_private=False)
        serializer = SongDisplaySerializer(songs, many=True)
        return Response({"data":serializer.data,"message":"all public songs displayed"}, status=status.HTTP_200_OK)

class AllPublicPlaylistsAPI(APIView):
    renderer_classes = [UserRenderer]

    def get(self,format=None):
        playlists = Playlist.objects.filter(is_private=False)
        serializer = PlaylistDisplaySerializer(playlists, many=True)
        return Response({"data":serializer.data,"message":"all public playlists displayed"}, status=status.HTTP_200_OK)


class PublicSongsFromPlaylistAPI(APIView):
    renderer_classes = [UserRenderer]

    def get(self, request,pk):
        try:
            playlist = Playlist.objects.get(pk=pk)
        except Playlist.DoesNotExist:
            return Response({'message': 'Playlist not found'}, status=status.HTTP_404_NOT_FOUND)
        if playlist.is_private:
            return Response({'message': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
        if  playlist.songs.count() == 0:
            return Response({'message': 'No songs in playlist'}, status=status.HTTP_404_NOT_FOUND)
        songs = playlist.songs.filter(is_private=False)
        serializer = SongDisplaySerializer(songs, many=True)

        return Response({"data":serializer.data,"message":"all public songs from playlist displayed"}, status=status.HTTP_200_OK)

class SongSearchAPI(APIView):
    renderer_classes = [UserRenderer]


    def get(self, request):
        query = request.GET.get('query')

        if not query:
            return Response({'message': 'No search parameters provided'}, status=status.HTTP_400_BAD_REQUEST)

        songs = Song.objects.filter(is_private=False)

        q_objects = Q()


        q_objects |= Q(name__icontains=query)
        q_objects |= Q(language__name__icontains=query)
        q_objects |= Q(genre__name__icontains=query)
        q_objects |= Q(mood__name__icontains=query)
        q_objects |= Q(artist__username__icontains=query)

        songs = songs.filter(q_objects).distinct()
        if not songs:
            return Response({'message': 'No songs found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = SongDisplaySerializer(songs, many=True)
        return Response({"data": serializer.data, "message": "Songs matching the search criteria"}, status=status.HTTP_200_OK)


class GetSong(APIView):
    renderer_classes = [UserRenderer]

    def get(self,request,pk):
        try:
            song = Song.objects.get(pk=pk)
        except Song.DoesNotExist:
            return Response({'message': 'Song not found'}, status=status.HTTP_404_NOT_FOUND)
        if request.user == song.artist or not song.is_private:
            serializer = SongSerializer(song)
            return Response({"data": serializer.data, "message": "Song found"}, status=status.HTTP_200_OK)

        return Response({'message': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)


class FavouriteSongsAPI(APIView):
    renderer_classes = [UserRenderer]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, song_id):
        favourite = Favourite.objects.get(user=request.user)
        song = Song.objects.get(id=song_id)
        favourite.song.add(song)
        return Response({"message": "Song added to favourites"}, status=status.HTTP_200_OK)

    def delete(self, request, song_id):
        favourite = Favourite.objects.get(user=request.user)
        song = Song.objects.get(id=song_id)
        if song in favourite.song.all():
            favourite.song.remove(song)
            return Response({"message": "Song removed from favourites"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Song is not in your favorites"}, status=status.HTTP_400_BAD_REQUEST)


class GetFavoriteSongsAPI(APIView):
    renderer_classes = [UserRenderer]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        favourite = Favourite.objects.get(user=request.user)
        songs = favourite.song.all()
        if songs.count() == 0 :
            return Response({'message': 'No songs found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = SongDisplaySerializer(songs, many=True)
        return Response({"data": serializer.data, "message": "Songs found"}, status=status.HTTP_200_OK)


class FavouritePlaylistsAPI(APIView):
    renderer_classes = [UserRenderer]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, playlist_id):
        favourite = Favourite.objects.get(user=request.user)
        playlist = Playlist.objects.get(id=playlist_id)
        favourite.playlist.add(playlist)
        return Response({"message": "Playlist added to favourites"}, status=status.HTTP_200_OK)

    def delete(self, request, playlist_id):
        favourite = Favourite.objects.get(user=request.user)
        playlist = Playlist.objects.get(id=playlist_id)
        if playlist in favourite.playlist.all():
            favourite.playlist.remove(playlist)
            return Response({"message": "Playlist removed from favourites"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Playlist is not in your favorites"}, status=status.HTTP_400_BAD_REQUEST)


class GetFavoritePlaylistsAPI(APIView):
    renderer_classes = [UserRenderer]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        favourite = Favourite.objects.get(user=request.user)
        playlists = favourite.playlist.all()
        serializer = PlaylistSerializer(playlists, many=True)
        return Response({"data": serializer.data, "message": "Playlists found"}, status=status.HTTP_200_OK)
