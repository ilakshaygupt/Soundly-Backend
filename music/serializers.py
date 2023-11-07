from rest_framework import serializers

from .models import Playlist, Song


class PlaylistSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True,error_messages={'required': 'Please enter a name'})
    description = serializers.CharField(required=True,error_messages={'required': 'Please enter a description'})
    thumbnail_url = serializers.URLField(required=False)
    class Meta:
        model = Playlist
        fields = '__all__'

class SongCreateSerializer(serializers.ModelSerializer):
    language_name = serializers.CharField(required=True,error_messages={'required': 'Please enter a language'})
    mood_name = serializers.CharField(required=True,error_messages={'required': 'Please enter a mood'})
    genre_name = serializers.CharField(required=True,error_messages={'required': 'Please enter a genre'})

    class Meta:
        model = Song
        fields =  '__all__'

class SongDisplaySerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True,error_messages={'required': 'Please enter a name'})
    artist = serializers.CharField(required=True,error_messages={'required': 'Please enter an artist'})
    language = serializers.CharField(required=True,error_messages={'required': 'Please enter a language'})
    mood = serializers.CharField(required=True,error_messages={'required': 'Please enter a mood'})
    genre = serializers.CharField(required=True,error_messages={'required': 'Please enter a genre'})
    song_url = serializers.URLField(required=True,error_messages={'required': 'Please enter a song url'})
    thumbnail_url = serializers.URLField(required=True,error_messages={'required': 'Please enter a thumbnail url'})

    class Meta:
        model = Song
        fields =  '__all__'

class SongSerializer3(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields =  ['name']
