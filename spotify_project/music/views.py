from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, FormView, CreateView, DeleteView

import music
from music.forms import AddMusicForm, PlaylistForm
from music.models import Genre, Music, History, Playlist, Album


# Create your views here.
@method_decorator(
    login_required(login_url='sign_in_page_name'),
    name='dispatch'
)
class CategoryView(ListView):
    template_name = 'music/index.html'
    model = Genre
    context_object_name = 'genres'

@method_decorator(
    login_required(login_url='sign_in_page_name'),
    name='dispatch'
)
class AlbumsView(ListView):
    template_name = 'music/albums.html'
    model = Album
    context_object_name = 'albums'



@method_decorator(
    login_required(login_url='sign_in_page_name'),
    name='dispatch'
)
class GenreDetail(DetailView):
    model = Genre
    context_object_name = 'genre'
    template_name = 'music/genre_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        genre = context.get('genre')
        context['musics'] = genre.musics.all()
        return context
@method_decorator(
    login_required(login_url='sign_in_page_name'),
    name='dispatch'
)
class AlbumDetail(DetailView):
    model = Album
    context_object_name = 'album'
    template_name = 'music/album_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        album = context.get('album')
        context['musics'] = album.musics.all()
        return context
@method_decorator(
    login_required(login_url='sign_in_page_name'),
    name='dispatch'
)
class MusicDetail(DetailView):
    template_name = 'music/music.html'
    model = Music
    context_object_name = 'music'

    def get(self, request, *args, **kwargs):
        History.objects.create(
            music=Music.objects.get(pk=self.kwargs['pk']),
            user=self.request.user
        )
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        music = Music.objects.get(pk=self.kwargs['pk'])
        playlist_id = self.request.POST['playlist']
        playlist = Playlist.objects.get(pk=playlist_id)
        # print(playlist)
        # new_playlist_music = Playlist.musics
        # print(new_playlist_music)
        # playlist = request.get('playlist_id')
        # Playlist.objects.create(
        #     musics=music
        # )
        playlist.musics.add(music)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        music = context.get('music')
        genres = music.genres.all()
        context['genres'] = genres
        context['genres_str'] = ', '.join(map(lambda genre: genre.name,
                                              genres))
        context['playlists'] = self.request.user.playlists.all()
        return context


@method_decorator(
    login_required(login_url='sign_in_page_name'),
    name='dispatch'
)
class HistoryView(ListView):
    model = History
    context_object_name = 'histories'
    template_name = 'music/history.html'
    paginate_by = 15

    def get_queryset(self):
        return History.objects.filter(user=self.request.user).order_by('-listened_at')


@method_decorator(
    login_required(login_url='sign_in_page_name'),
    name='dispatch'
)
class UploadMusicView(CreateView):
    template_name = 'music/upload_music.html'
    model = Music
    form_class = AddMusicForm

    def form_valid(self, form):
        music = form.save(commit=False)
        music.author = self.request.user
        music.save()
        form.save_m2m()
        return redirect('index')


@method_decorator(
    login_required(login_url='sign_in_page_name'),
    name='dispatch'
)
class PlaylistView(ListView):
    model = Playlist
    context_object_name = 'playlists'
    template_name = 'music/playlists.html'

    def get_queryset(self):
        return Playlist.objects.filter(author=self.request.user).order_by('-created_at')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        new_playlists = []
        for playlist in ctx['playlists']:
            musics = playlist.musics.all()
            new_playlist = {
                'id': playlist.id,
                'name': playlist.name,
                'musics': musics,
                'created_at': playlist.created_at,
                'image': musics[0].image.url if len(musics) > 0 else '/media/default.jpg',
            }
            new_playlists.append(new_playlist)
        ctx['new_playlists'] = new_playlists
        ctx['form'] = PlaylistForm()
        return ctx

    def post(self, *args, **kwargs):
        form = PlaylistForm(self.request.POST)
        if form.is_valid():
            playlist = form.save(commit=False)
            playlist.author = self.request.user
            playlist.save()
        return redirect('playlists')


@method_decorator(
    login_required(login_url='sign_in_page_name'),
    name='dispatch'
)
class PlaylistDetailView(DetailView):
    template_name = 'music/playlist_detail.html'
    model = Playlist
    context_object_name = 'playlist'

    def get(self, request, *args, **kwargs):
        playlist = Playlist.objects.get(pk=self.kwargs['pk'])
        if request.user.id != playlist.author.id:
            if not playlist.is_public:
                return redirect('error_page')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        playlist = Playlist.objects.get(pk=self.kwargs['pk'])
        music_id = self.request.POST['music_id']
        music = Music.objects.get(pk=music_id)
        if playlist.author.id != request.user.id:
            return redirect('error_page')
        playlist.musics.remove(music)
        return super().get(request, *args, **kwargs)


@method_decorator(
    login_required(login_url='sign_in_page_name'),
    name='dispatch'
)
class PlaylistDeleteView(DeleteView):
    template_name = 'music/delete_confirm.html'
    model = Playlist
    context_object_name = 'playlist'
    # success_url = reverse_lazy('playlists')

    def post(self, request, *args, **kwargs):
        playlist = Playlist.objects.get(pk=self.kwargs['pk'])
        if playlist.author.id != request.user.id:
            return redirect('error_page')
        playlist.delete()
        return redirect('playlists')
