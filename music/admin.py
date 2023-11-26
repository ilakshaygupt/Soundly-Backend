from django.contrib import admin

from .models import *


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ("id", "name")

    list_per_page = 25


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ("name", "uploader", "genre", "language", "mood", "date_added", "id")
    list_per_page = 25


admin.site.register(Favourite)
admin.site.register(Language)
admin.site.register(Genre)
admin.site.register(Mood)
admin.site.register(Artist)
admin.site.register(RecentlyPlayed)
# pass=admin
