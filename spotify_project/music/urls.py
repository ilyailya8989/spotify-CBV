from urls import path
from views.generic import TemplateView

from music import views

urlpatterns = [
    path('', views.CategoryView.as_view(), name='index'),
    path('error/', TemplateView.as_view(template_name="music/error.html"), name='error_page'),
    path('genre/<int:pk>', views.GenreDetail.as_view(), name='genre'),
    path('music/<int:pk>', views.MusicDetail.as_view(), name='music'),
    path('history/', views.HistoryView.as_view(), name='history'),
    path('upload-music/', views.UploadMusicView.as_view(), name='upload_music'),
    path('playlists/', views.PlaylistView.as_view(), name='playlists'),
    path('playlists/<int:pk>', views.PlaylistDetailView.as_view(), name='playlist_detail'),
    path("playlist/<int:pk>/delete", views.PlaylistDeleteView.as_view(), name='playlist_remove'),
    path('albums', views.AlbumsView.as_view(), name='albums'),
    path('albums/<int:pk>', views.AlbumDetail.as_view(), name='albums_detail'),

]
