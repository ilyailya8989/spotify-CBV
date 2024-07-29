from django.contrib import admin

from music.models import Genre, Music, Album, Playlist, History

# Register your models here.
admin.site.register([Genre, Music, Album, Playlist, History])
