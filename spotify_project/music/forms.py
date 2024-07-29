from django import forms

from music.models import Music, Playlist


class AddMusicForm(forms.ModelForm):
    class Meta:
        model = Music
        fields = 'name', 'image', 'file', 'album', 'genres'


class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = 'name', 'is_public'
