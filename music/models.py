from cloudinary.models import CloudinaryField
from django.db import models

from accounts.models import MyUser


class Language(models.Model):
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Genre(models.Model):
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Mood(models.Model):
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Artist(models.Model):
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Song(models.Model):
    name = models.CharField(max_length=100)
    artist = models.ForeignKey(Artist,blank=True,default=None,null=True,on_delete=models.CASCADE)
    uploader = models.ForeignKey(MyUser,blank=True,on_delete=models.CASCADE,default=None,null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, blank=True, null=True)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, blank=True, null=True)
    mood = models.ForeignKey(Mood, on_delete=models.SET_NULL, blank=True, null=True)
    song_url = models.URLField(blank=True,null=True,default=None)
    thumbnail_url = models.URLField(blank=True,null=True,default=None)
    is_private = models.BooleanField(default=False)
    def __str__(self):
        return self.name


class Playlist(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    thumbnail_url = models.URLField(blank=True,null=True,default=None)
    uploader = models.ForeignKey(MyUser,on_delete=models.CASCADE,blank=True,default=None,null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    is_private = models.BooleanField(default=False)
    songs=models.ManyToManyField(Song,blank=True,default=None,null=True)
    def __str__(self):
        return self.name



class Favourite(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE,blank=True,default=None,null=True)
    language = models.ManyToManyField(Language, blank=True, null=True)
    playlist = models.ManyToManyField(Playlist, blank=True,default=None,null=True)
    song = models.ManyToManyField(Song, blank=True,default=None,null=True)
    def __str__(self):
        return self.user.username
