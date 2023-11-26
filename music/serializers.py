from rest_framework import serializers

from .models import *
import re
from rest_framework.response import Response
from rest_framework import status
import cloudinary

class PlaylistSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, error_messages={
                                 'required': 'Please enter a name'})
    description = serializers.CharField(required=True, error_messages={
                                        'required': 'Please enter a description'})
    thumbnail_url = serializers.URLField(required=False)

    class Meta:
        model = Playlist
        fields = '__all__'


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

    class Meta:
        model = Playlist
        fields = ['name', 'id', 'description', 'thumbnail_url', 'uploader']


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
    def create(self, validated_data):
        # Extracting values from validated_data
        language_name = validated_data.pop('language_name', None)
        mood_name = validated_data.pop('mood_name', None)
        genre_name = validated_data.pop('genre_name', None)
        artist_name = validated_data.pop('artist_name', None)

        # Extract files from request.FILES
        audio_file = self.context['request'].FILES.get('audio')
        thumbnail_file = self.context['request'].FILES.get('thumbnail')
        lyrics_file = self.context['request'].FILES.get('lyrics')

        # Your file validation and cloudinary upload logic here
        if audio_file:
            if audio_file.size > 7000000 or audio_file.content_type != 'audio/mpeg':
                raise serializers.ValidationError({'message': 'Invalid audio file'})
        else:
            raise serializers.ValidationError({'message': 'Audio file is required'})

        if thumbnail_file:
            if thumbnail_file.size > 4000000 or thumbnail_file.content_type not in ['image/png', 'image/jpeg']:
                raise serializers.ValidationError({'message': 'Invalid thumbnail file'})
        else:
            raise serializers.ValidationError({'message': 'Thumbnail file is required'})

        if lyrics_file:
            if lyrics_file.size > 4000000 or not re.search(r'\.srt$', lyrics_file.name, re.IGNORECASE):
                raise serializers.ValidationError({'message': 'Invalid lyrics file'})

        # Cloudinary upload logic
        audio_response = cloudinary.uploader.upload(audio_file, secure=True, resource_type='video')
        audio_url = audio_response.get('url')

        thumbnail_response = cloudinary.uploader.upload(thumbnail_file, secure=True)
        thumbnail_url = thumbnail_response.get('url')

        if lyrics_file:
            lyrics_response = cloudinary.uploader.upload(lyrics_file, secure=True, resource_type='raw')
            lyrics_url = lyrics_response.get('url')
        else:
            lyrics_url = None
        # Create or get related objects
        language, _ = Language.objects.get_or_create(name=language_name)
        mood, _ = Mood.objects.get_or_create(name=mood_name)
        genre, _ = Genre.objects.get_or_create(name=genre_name)
        artist, _ = Artist.objects.get_or_create(name=artist_name)

        # Create the Song instance
        song = Song.objects.create(
            uploader=self.context['request'].user,
            language=language,
            mood=mood,
            genre=genre,
            artist=artist,
            song_url=audio_url,
            thumbnail_url=thumbnail_url,
            lyrics_url=lyrics_url,
            **validated_data
        )
        return song

    def validate_lyrics(self, value):
        if value and value.size > 4000000:
            raise serializers.ValidationError('Lyrics file size must be less than 4MB')
        if value and not re.search(r'\.srt$', value.name, re.IGNORECASE):
            raise serializers.ValidationError('Lyrics file type must be srt')
        return value
    def validate_mood_name(self, value):
        if len(value) == 0:
            raise serializers.ValidationError("Please enter a valid mood name")
        if not Mood.objects.filter(name=value).exists():
            Mood.objects.create(name=value)
        return value
    
    def validate_genre_name(self, value):
        if len(value) == 0:
            raise serializers.ValidationError("Please enter a valid genre name")
        if not Genre.objects.filter(name=value).exists():
            Genre.objects.create(name=value)
        return value
    def validate_language_name(self, value):
        if len(value) == 0:
            raise serializers.ValidationError("Please enter a valid language name")
        if not Language.objects.filter(name=value).exists():
            Language.objects.create(name=value)
        return value
    def validate_artist_name(self, value):
        if len(value) == 0:
            raise serializers.ValidationError("Please enter a valid artist name")
        if not Artist.objects.filter(name=value).exists():
            Artist.objects.create(name=value)
        return value
    
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

    class Meta:
        model = Song
        fields = ['id', 'name', 'song_url', 'thumbnail_url','is_liked','lyrics_url','song_duration']
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
    
