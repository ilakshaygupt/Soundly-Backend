
from rest_framework.response import Response
from .models import  Playlist , Song , Language , Mood ,Genre
from rest_framework import status
from rest_framework.views import APIView
from music.serializers import PlaylistSerializer ,SongSerializer , SongSerializer2 ,SongSerializer3
from accounts.renderers import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser


class SongAPI(APIView):
    serializer_class = SongSerializer2
    renderer_classes = [UserRenderer]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None):
        serializer = SongSerializer(data=request.data)
        if serializer.is_valid():
            artist = request.user
            audio_url = None
            if 'audio' in request.FILES:
                audio = request.FILES['audio']
                audio_response = cloudinary.uploader.upload(audio, secure=True, resource_type='video')
                audio_url = audio_response.get('url')

            thumbnail_url = None
            if 'thumbnail' in request.FILES:
                thumbnail = request.FILES['thumbnail']
                thumbnail_response = cloudinary.uploader.upload(thumbnail, secure=True)
                thumbnail_url = thumbnail_response.get('url')

            # Get language_id and mood_id based on the received names
            language_name = serializer.validated_data.pop('language_name', None)
            mood_name = serializer.validated_data.pop('mood_name', None)
            genre_name = serializer.validated_data.pop('genre_name', None)

            try:
                language = Language.objects.get(name=language_name)
            except Language.DoesNotExist:
                return Response({'message': f'Language with name "{language_name}" not found.'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                mood = Mood.objects.get(name=mood_name)
            except Mood.DoesNotExist:
                return Response({'message': f'Mood with name "{mood_name}" not found.'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                genre = Genre.objects.get(name=genre_name)
            except Genre.DoesNotExist:
                return Response({'message': f'Genre with name "{genre_name}" not found.'}, status=status.HTTP_400_BAD_REQUEST)

            # Create the Song instance using serializer.validated_data
            song = Song.objects.create(
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



    def get(self, request, pk=None, format=None):
        if pk is not None:
            try:
                song = Song.objects.get(id=pk)
                serializer = SongSerializer2(song)
                return Response({"data":serializer.data,"message": "found song"})
            except Song.DoesNotExist:
                return Response({'message': 'Song not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            songs = Song.objects.all()
            serializer = SongSerializer2(songs, many=True)
            return Response({"data":serializer.data,"message": "all songs"})

    def put(self, request, pk, format=None):
        try:
            song = Song.objects.get(id=pk)
        except Song.DoesNotExist:
            return Response({'message': 'Song not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = SongSerializer3(song, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Song updated successfully'
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        try:
            song = Song.objects.get(id=pk)
        except Song.DoesNotExist:
            return Response({'message': 'Song not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = SongSerializer3(song, data=request.data, partial=True)
        if serializer.is_valid():
            if song.artist != request.user:
                return Response({'message': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
            serializer.save()
            return Response({
                'message': 'Song partially updated'
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        try:
            song = Song.objects.get(id=pk)
        except Song.DoesNotExist:
            return Response({'message': 'Song not found'}, status=status.HTTP_404_NOT_FOUND)
        if song.artist != request.user:
            return Response({'message': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
        song.delete()
        return Response({'message': 'Song deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


import cloudinary
from rest_framework.parsers import MultiPartParser, FormParser

class PlaylistAPI(APIView):
    serializer_class = PlaylistSerializer
    renderer_classes = [UserRenderer]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    def post(self, request, format=None):
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


    def get(self, request, pk=None, format=None):
        if pk:
            try:
                playlist = Playlist.objects.get(id=pk)
                if playlist.artist == request.user:
                    serializer = PlaylistSerializer(playlist)
                    return Response({"data": serializer.data, "message": "found playlist"})
                else:
                    return Response({'message': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
            except Playlist.DoesNotExist:
                return Response({'message': 'Playlist not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            playlists = Playlist.objects.filter(artist=request.user)
            serializer = PlaylistSerializer(playlists, many=True)
            return Response({"data" :serializer.data,"message": "all user playlist"})

    def put(self, request, pk, format=None):
        try:
            playlist = Playlist.objects.get(pk=pk)
        except Playlist.DoesNotExist:
            return Response({'message': 'Playlist not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = PlaylistSerializer(playlist, data=request.data)
        if serializer.is_valid():

            # if 'thumbnail' in request.FILES:
            #     thumbnail = request.FILES['thumbnail']
            #     thumbnail_response = cloudinary.uploader.upload(thumbnail, secure=True)
            #     thumbnail_url = thumbnail_response.get('url')
            #     playlist.thumbnail = thumbnail_url

            serializer.save(artist=request.user)
            return Response({
                'message': 'Playlist updated successfully'
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def patch(self, request, pk, format=None):
        try:
            playlist = Playlist.objects.get(pk=pk)
        except Playlist.DoesNotExist:
            return Response({'message': 'Playlist not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = PlaylistSerializer(playlist, data=request.data, partial=True)
        if serializer.is_valid():
            # thumbnail_url = playlist.thumbnail_url
            # if 'thumbnail' in request.FILES:
            #     thumbnail = request.FILES['thumbnail']
            #     thumbnail_response = cloudinary.uploader.upload(thumbnail, secure=True)
            #     thumbnail_url = thumbnail_response.get('url')
            #     playlist.thumbnail = thumbnail_url

            serializer.save()
            return Response({
                'message': 'Playlist partially updated'
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        try:
            playlist = Playlist.objects.get(pk=pk)
        except Playlist.DoesNotExist:
            return Response({'message': 'Playlist not found'}, status=status.HTTP_404_NOT_FOUND)

        playlist.delete()
        return Response({'message': 'Playlist deleted'}, status=status.HTTP_204_NO_CONTENT)

class PlaylistSongAPI(APIView):#display all songs from a playlist
    renderer_classes = [UserRenderer]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, format=None, song_pk=None):
        try:
            playlist = Playlist.objects.get(pk=pk)
        except Playlist.DoesNotExist:
            return Response({'message': 'Playlist not found'}, status=status.HTTP_404_NOT_FOUND)

        songs = playlist.songs.all()
        serializer = SongSerializer2(songs, many=True)

        return Response({"data":serializer.data,"message":"all songs displayed"}, status=status.HTTP_200_OK)



class AddSongToPlaylistAPI(APIView):
    renderer_classes = [UserRenderer]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, pk,song_pk, format=None):
        try:
            playlist = Playlist.objects.get(pk=pk)
        except Playlist.DoesNotExist:
            return Response({'message': 'Playlist not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            song = Song.objects.get(id=song_pk)
        except Song.DoesNotExist:
            return Response({'message': 'Song not found'}, status=status.HTTP_404_NOT_FOUND)
        playlist.songs.add(song)
        return Response({'message': 'Song added successfully to the playlist'}, status=status.HTTP_201_CREATED)

    def delete(self, request, pk,song_pk, format=None):
        try:
            playlist = Playlist.objects.get(pk=pk)
        except Playlist.DoesNotExist:
            return Response({'message': 'Playlist not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            song = Song.objects.get(id=song_pk)
        except Song.DoesNotExist:
            return Response({'message': 'Song not found'}, status=status.HTTP_404_NOT_FOUND)
        playlist.songs.remove(song)
        return Response({'message': 'Song removed from the playlist'}, status=status.HTTP_204_NO_CONTENT)


#Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAxNzAwMzkyLCJpYXQiOjE2OTkxMDgzOTIsImp0aSI6ImIwNjE3MTJlY2MwNDQ0YmFiMDhmMjYzOGQ0MmQ3ZDVjIiwidXNlcl9pZCI6ImFkbWluIn0.S6YcBuB-BaIsMchGyLIqnWe8pkO_4Zp0v-ZwcrP1Ca4
