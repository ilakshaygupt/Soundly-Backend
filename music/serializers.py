from rest_framework import serializers
from .models import Playlist
from .models import Song
class PlaylistSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True,error_messages={'required': 'Please enter a name'})
    description = serializers.CharField(required=True,error_messages={'required': 'Please enter a description'})
    thumbnail_url = serializers.URLField(required=False)
    class Meta:
        model = Playlist
        fields = '__all__'

class SongSerializer(serializers.ModelSerializer):
    language_name = serializers.CharField(required=True,error_messages={'required': 'Please enter a language'})
    mood_name = serializers.CharField(required=True,error_messages={'required': 'Please enter a mood'})
    genre_name = serializers.CharField(required=True,error_messages={'required': 'Please enter a genre'})

    class Meta:
        model = Song
        fields =  '__all__'

class SongSerializer2(serializers.ModelSerializer):

    class Meta:
        model = Song
        fields =  '__all__'

class SongSerializer3(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields =  ['name']
