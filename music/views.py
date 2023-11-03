
from rest_framework.response import Response
from .models import Song, Playlist
from rest_framework import status
from rest_framework.views import APIView
from music.serializers import SongSerializer, PlaylistSerializer
from accounts.renderers import UserRenderer
# Create your views here.

# class Playlist(generics.ListAPIView):
#     queryset = Playlist.objects.all()
#     serializer_class = PlaylistSerializer


# class Song(generics.ListAPIView):
#     queryset = Song.objects.all()
#     serializer_class = SongSerializer

# class CreatePlaylistView(APIView):
#  serializer_class = CreatePlaylistSerializer
class SongAPI(APIView):
    serializer_class = SongSerializer


    def post(self, request, format=None):

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            obj = serializer.create(serializer.validated_data)
            obj.save()
            return Response({
                'status': 200,
                'message': 'song added successfully in playlist'

            })
        return Response(serializer.errors)
    
    def get(self, request, pk=None, format=None):
        song = Song.objects.all()
        serializer = SongSerializer(song, many=True)
        return Response(serializer.data)

  
class Individual(APIView):
    
    def get(self, request, pk=None, format=None):
        id = pk
        if id is not None:
            song = Song.objects.get(id=id)
            serializer = SongSerializer(song)
            return Response(serializer.data)

        song = Song.objects.all()
        serializer = SongSerializer(song, many=True)
        return Response(serializer.data)

    # return Response(serializer.errors)


# def put(self, request,pk, format=None):
#             id=pk
#             song=Song.objects.get(pk=id)
#             serializer=SongSerializer(song,data=request.data)
#             if serializer.is_valid():
#              serializer.save()
#             return Response ({
#                         'status':200,
#                         'message':'song updated successfully'

#                     })
    # def delete(self,request,pk,format=None):
    #   print("jfdlkj")
    # id=pk

    #   song=Song.objects.get(id=pk)
    #   song.delete()

    #   return Response({
    #     'message':'deleted',
    #     'status':200

    # })

    def delete(self, request, pk, format=None):
        song = Song.objects.get(id=pk)
        print(song)
        song.delete()
        print(song)
        return Response({
            'message': 'deleted',
            'status': 200
            

        })
    


class PlaylistAPI(APIView):

    serializer_class = PlaylistSerializer

    def post(self, request, format=None):

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():

            obj = serializer.create(serializer.validated_data)
            obj.save()
            return Response({
                'status': 200,
                'message': 'playlist created successfully'

            })

            # Playlist.save()

    def get(self, request, pk=None, format=None):
        id = pk
        if id is not None:
            play = Playlist.objects.get(id=id)
            serializer = PlaylistSerializer(play)
            return Response(serializer.data)

        play = Playlist.objects.all()
        serializer = PlaylistSerializer(play, many=True)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        id = pk
        play = Playlist.objects.get(pk=id)
        serializer = PlaylistSerializer(play, data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response({
            'status': 200,
            'message': 'playlist updated successfully'

        })
        
    def patch(self, request, pk, format=None):
        id = pk
        play = Playlist.objects.get(pk=id)
        serializer = SongSerializer(play, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response({
            'status': 200,
            'message': 'playlist  partially updated '

        })
    def delete(self,request,pk,format=None):
        id=pk
        play=Playlist.objects.get(pk=id)
        play.delete()
        return Response({
            'message':'deleted'
            
        })


# # class SongAPI(APIView):
# #         serializer_class = SongSerializer

#         def get(self, request, format=None):
#          song =Song.object.all()
#          serializer=SongSerializer(song,many=True)
#          return Response(serializer.data)

#          return Response(serializer.errors)


# class  Add_song_to_playlist(APIView):
#  def post(self,request):
#     # try:
#         print("hellp")
#         playlist = request.data.get('playlist')
      
        
#         print(type(playlist))
#         playlist = Playlist.objects.get(id=playlist)
#         song_id=request.data.get('song_id')
#         song = Song.objects.get(id=song_id)
#         playlist.song.add(song)
       
#     # except (Playlist.DoesNotExist, Song.DoesNotExist):
#     #     return Response(status=404)

#         # playlist.Song.add(song_id)
#         playlist.save()

#         return Response(PlaylistSerializer(playlist).data)

