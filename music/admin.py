from django.contrib import admin
from .models import Playlist,Song




# admin.site.register(Playlist)
# admin.site.register(Song)


# Register your models here.
@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
     list_display = ('id', 'name', 'date_created')
    
@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'artist', )
#username=prashant
#pass=admin