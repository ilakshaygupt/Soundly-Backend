from datetime import timedelta

from rest_framework import serializers

from .models import Favourite, Playlist, Song


class PlaylistSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, error_messages={
                                 'required': 'Please enter a name'})
    description = serializers.CharField(required=True, error_messages={
                                        'required': 'Please enter a description'})
    thumbnail_url = serializers.URLField(required=False)
    totalduration = serializers.SerializerMethodField()
    class Meta:
        model = Playlist
        fields = '__all__'
    def get_totalduration(self, obj):
        total_duration_seconds = 0

        for song in obj.songs.all():
            minutes, seconds = map(int, song.song_duration.split(':'))
            duration_seconds = minutes * 60 + seconds
            total_duration_seconds += duration_seconds

        total_duration = str(timedelta(seconds=total_duration_seconds))

        return total_duration


class ChangePlaylistSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, error_messages={
                                 'required': 'Please enter a name'})
    description = serializers.CharField(required=True, error_messages={
                                        'required': 'Please enter a description'})
    thumbnail_url = serializers.URLField(required=False)

    class Meta:
        model = Playlist
        fields = ['name', 'description', 'thumbnail_url']


class PlaylistDisplaySerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, error_messages={
                                 'required': 'Please enter a name'})
    description = serializers.CharField(required=True, error_messages={
                                        'required': 'Please enter a description'})
    thumbnail_url = serializers.URLField(required=False)
    uploader = serializers.CharField(required=True, error_messages={
                                     'required': 'Please enter an uploader'})
    totalduration = serializers.SerializerMethodField()
    class Meta:
        model = Playlist
        fields = ['name', 'id', 'description', 'thumbnail_url', 'uploader','totalduration']
    def get_totalduration(self, obj):
        total_duration_seconds = 0

        for song in obj.songs.all():
            minutes, seconds = map(int, song.song_duration.split(':'))
            duration_seconds = minutes * 60 + seconds
            total_duration_seconds += duration_seconds

        total_duration = str(timedelta(seconds=total_duration_seconds))

        return total_duration


class SongCreateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, error_messages={
                                 'required': 'Please enter a name'})
    language_name = serializers.CharField(required=True, error_messages={
                                          'required': 'Please enter a language'})
    mood_name = serializers.CharField(required=True, error_messages={
                                      'required': 'Please enter a mood'})
    genre_name = serializers.CharField(required=True, error_messages={
                                       'required': 'Please enter a genre'})
    artist_name = serializers.CharField(required=True, error_messages={
                                        'required': 'Please enter an artist'})

    class Meta:
        model = Song
        fields = '__all__'


class SongDisplaySerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, error_messages={
                                 'required': 'Please enter a name'})
    uploader = serializers.CharField(required=True, error_messages={
                                     'required': 'Please enter an uploader'})
    language = serializers.CharField(required=True, error_messages={
                                     'required': 'Please enter a language'})
    mood = serializers.CharField(required=True, error_messages={
                                 'required': 'Please enter a mood'})
    genre = serializers.CharField(required=True, error_messages={
                                  'required': 'Please enter a genre'})
    thumbnail_url = serializers.URLField(required=True, error_messages={
                                         'required': 'Please enter a thumbnail url'})
    artist = serializers.CharField(required=True, error_messages={
                                   'required': 'Please enter an artist'})
    is_private = serializers.BooleanField(required=True, error_messages={
                                            'required': 'Please enter a public status'}
    )
    is_liked = serializers.SerializerMethodField()
    song_duration = serializers.CharField(required=False)
    
    class Meta:
        model = Song
        fields = ['name', 'id', 'uploader', 'language','song_duration',
                  'mood', 'genre', 'thumbnail_url', 'artist', 'is_private','is_liked']
    def get_is_liked(self, obj):
        user = self.context.get('user')
        return Favourite.objects.filter(user=user, song=obj).exists()

class ChangeSongSerializer(serializers.ModelSerializer):
    is_private = serializers.BooleanField(required=True, error_messages={
                                          'required': 'Please enter a public status'})

    class Meta:
        model = Song
        fields = ['name', 'is_private']


class SongSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, error_messages={
                                 'required': 'Please enter a name'})
    song_url = serializers.URLField(required=True, error_messages={
                                    'required': 'Please enter an audio url'})
    thumbnail_url = serializers.URLField(required=True, error_messages={
                                         'required': 'Please enter a thumbnail url'})
    is_liked = serializers.SerializerMethodField()
    lyrics_url = serializers.URLField(required=False)
    song_duration = serializers.CharField(required=False)
    lyrics_json = serializers.CharField(required=False)
    class Meta:
        model = Song
        fields = ['id', 'name', 'song_url', 'thumbnail_url','is_liked','lyrics_url','song_duration','lyrics_json']
    def get_is_liked(self, obj):
        user = self.context.get('user')
        return Favourite.objects.filter(user=user, song=obj).exists()


class artistSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, error_messages={
                                 'required': 'Please enter a name'})
    thumbnail_url = serializers.URLField(required=False, error_messages={
                                         'required': 'Please enter a thumbnail url'})
    class Meta:
        model = Song
        fields = ['id', 'name','thumbnail_url']

class AddFavArtists(serializers.ModelSerializer):
    artist_names = serializers.ListField(child = serializers.CharField())
    class Meta:
        model = Favourite
        fields = ['artist_names']
    def validate(self, data):
        if len(data['artist_names']) == 0:
            raise serializers.ValidationError("Please enter atleast one artist name")
        return data
    def validate_artist_names(self, value):
        for name in value:
            if len(name) == 0:
                raise serializers.ValidationError("Please enter a valid artist name")
        if not all(isinstance(item, str) for item in value):
            raise serializers.ValidationError("Please enter a valid artist name")
        return value
    
class LanguageSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, error_messages={
                                 'required': 'Please enter a name'})
   
    class Meta:
        model = Song
        fields = ['id', 'name']

class AddFavLanguages(serializers.ModelSerializer):
    language_names = serializers.ListField(child = serializers.CharField())
    class Meta:
        model = Favourite
        fields = ['language_names']
    def validate(self, data):
        if len(data['language_names']) == 0:
            raise serializers.ValidationError("Please enter atleast one language name")
        return data
    def validate_language_names(self, value):
        for name in value:
            if len(name) == 0:
                raise serializers.ValidationError("Please enter a valid language name")
        if not all(isinstance(item, str) for item in value):
            raise serializers.ValidationError("Please enter a valid language name")
        return value
    
