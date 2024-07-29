from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/genres/')

    def __str__(self):
        return self.name


class Album(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/album/')
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Music(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/music/')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='files/music/')
    album = models.ForeignKey(Album, on_delete=models.SET_NULL, null=True, related_name='musics')
    genres = models.ManyToManyField(Genre, related_name='musics')
    likes = models.ManyToManyField(User, related_name='liked_musics', blank=True)
    history = models.ManyToManyField(User, related_name='music_history', through="History", blank=True)

    def __str__(self):
        return self.name


class Playlist(models.Model):
    name = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='playlists')
    is_public = models.BooleanField(default=False)
    musics = models.ManyToManyField(Music, related_name='playlists', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class History(models.Model):
    music = models.ForeignKey(Music, related_name="user_history_music", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listened_at = models.DateTimeField(auto_now_add=True)
