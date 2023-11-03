from django.db import models

# Create your models here.
class Playlist(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    # song=models.ForeignKey(Song,on_delete=models.CASCADE,blank=True,default=None,null=True)

    def __str__(self):
        return self.name
    
class Song(models.Model):
    name = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)
    playlist=models.ForeignKey(Playlist,on_delete=models.CASCADE,blank=True,default=None,null=True)

    def __str__(self):
        return self.name
 
# class Playlist(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField()
#     date_created = models.DateTimeField(auto_now_add=True)
#     date_updated = models.DateTimeField(auto_now=True)
#     song=models.ForeignKey(Song,on_delete=models.CASCADE,blank=True,default=None,null=True)

#     def __str__(self):
#         return self.name    

