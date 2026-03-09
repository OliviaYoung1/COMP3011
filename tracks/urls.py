from django.urls import path
from .views import (
    TrackListView,
    TopTracksView,
    PlaylistListCreateView,
    PlaylistDetailView,
    PlaylistTrackCreateView,
    PlaylistTrackDeleteView,
    GenreListView,
)

urlpatterns = [
    path('tracks/', TrackListView.as_view(), name='track-list'),
    path('analytics/top-tracks/', TopTracksView.as_view(), name='top-tracks'),
    path('analytics/genres/', GenreListView.as_view(), name='genre-list'),
    path('playlists/', PlaylistListCreateView.as_view(), name='playlist-list-create'),
    path('playlists/<int:pk>/', PlaylistDetailView.as_view(), name='playlist-detail'),
    path('playlists/add-track/', PlaylistTrackCreateView.as_view(), name='playlist-add-track'),
    path('playlists/remove-track/<int:pk>/', PlaylistTrackDeleteView.as_view(), name='playlist-remove-track'),
]