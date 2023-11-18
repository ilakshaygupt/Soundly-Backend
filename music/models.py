import io

import requests
from cloudinary.models import CloudinaryField
from django.db import models
from pydub import AudioSegment

from accounts.models import MyUser


class Language(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Mood(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Artist(models.Model):
    name = models.CharField(max_length=100)
    thumbnail_url = models.URLField(blank=True, null=True, default='https://community.spotify.com/t5/image/serverpage/image-id/25294i2836BD1C1A31BDF2?v=v2')
    def __str__(self):
        return self.name


class Song(models.Model):
    name = models.CharField(max_length=100,db_index=True)
    artist = models.ForeignKey(
        Artist, blank=True, default=None, null=True, on_delete=models.CASCADE)
    uploader = models.ForeignKey(
        MyUser, blank=True, on_delete=models.CASCADE, default=None, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    language = models.ForeignKey(
        Language, on_delete=models.SET_NULL, blank=True, null=True)
    genre = models.ForeignKey(
        Genre, on_delete=models.SET_NULL, blank=True, null=True)
    mood = models.ForeignKey(
        Mood, on_delete=models.SET_NULL, blank=True, null=True)
    song_url = models.URLField(blank=True, null=True, default=None)
    thumbnail_url = models.URLField(blank=True, null=True, default=None)
    is_private = models.BooleanField(default=False)
    lyrics_url = models.URLField(blank=True, null=True, default=None)
    song_duration = models.CharField(max_length=10, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.song_url:
            duration = self.get_audio_duration_from_url(self.song_url)
            self.song_duration = self.convert_seconds_to_minutes(duration)

        super().save(*args, **kwargs)

    def get_audio_duration_from_url(self, audio_url):
        response = requests.get(audio_url)
        audio_data = response.content
        audio = AudioSegment.from_file(io.BytesIO(audio_data))
        duration_in_seconds = len(audio) / 1000.0
        return duration_in_seconds

    def convert_seconds_to_minutes(self, seconds):
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes:02d}:{seconds:02d}"
    def __str__(self):
        return self.name


class Playlist(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField(max_length=50, blank=True, null=True)
    thumbnail_url = models.URLField(blank=True, null=True, default='https://community.spotify.com/t5/image/serverpage/image-id/25294i2836BD1C1A31BDF2?v=v2')
    uploader = models.ForeignKey(
        MyUser, on_delete=models.CASCADE, blank=True, default=None, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    is_private = models.BooleanField(default=False)
    songs = models.ManyToManyField(Song, blank=True, default=None, null=True)
    

    def __str__(self):
        return self.name


class Favourite(models.Model):
    user = models.ForeignKey(
        MyUser, on_delete=models.CASCADE, blank=True, default=None, null=True)
    language = models.ManyToManyField(Language, blank=True, null=True)
    playlist = models.ManyToManyField(
        Playlist, blank=True, default=None, null=True)
    song = models.ManyToManyField(Song, blank=True, default=None, null=True)
    artist = models.ManyToManyField(
        Artist, blank=True, default=None, null=True)
    def __str__(self):
        return self.user.username

class RecentlyPlayed(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE,null=True,blank=True)
    song = models.ForeignKey(Song, on_delete=models.CASCADE,null=True,blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.song} - {self.timestamp}"
