from rest_framework import serializers

from .models import Playlist, Song


class PlaylistSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True,error_messages={'required': 'Please enter a name'})
    description = serializers.CharField(required=True,error_messages={'required': 'Please enter a description'})
    thumbnail_url = serializers.URLField(required=False)
    class Meta:
        model = Playlist
        fields = '__all__'

class ChangePlaylistSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True,error_messages={'required': 'Please enter a name'})
    description = serializers.CharField(required=True,error_messages={'required': 'Please enter a description'})
    thumbnail_url = serializers.URLField(required=False)
    class Meta:
        model = Playlist
        fields = ['name','description','thumbnail_url']
class PlaylistDisplaySerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True,error_messages={'required': 'Please enter a name'})
    description = serializers.CharField(required=True,error_messages={'required': 'Please enter a description'})
    thumbnail_url = serializers.URLField(required=False)
    artist = serializers.CharField(required=True,error_messages={'required': 'Please enter an artist'})
    class Meta:
        model = Playlist
        fields = ['name','id','description','thumbnail_url','artist']

class SongCreateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True,error_messages={'required': 'Please enter a name'})
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
    thumbnail_url = serializers.URLField(required=True,error_messages={'required': 'Please enter a thumbnail url'})

    class Meta:
        model = Song
        fields =  ['name','id','artist','language','mood','genre','thumbnail_url']

class ChangeSongSerializer(serializers.ModelSerializer):
    is_private = serializers.BooleanField(required=True,error_messages={'required': 'Please enter a public status'})

    class Meta:
        model = Song
        fields =  ['name','is_private']

class SongSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True,error_messages={'required': 'Please enter a name'})
    song_url = serializers.URLField(required=True,error_messages={'required': 'Please enter an audio url'})
    thumbnail_url = serializers.URLField(required=True,error_messages={'required': 'Please enter a thumbnail url'})

    class Meta:
        model = Song
        fields = ['id','name','song_url','thumbnail_url']
