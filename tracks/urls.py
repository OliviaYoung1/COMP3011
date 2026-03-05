from django.urls import path
from .views import (
    TrackListView,
    TrackDetailView,
    PopularityDistributionView,
    TopTracksView,
    GenrePopularityView,
    GenreEnergyDanceabilityView,
    PlaylistListCreateView,
    PlaylistDetailView,
    PlaylistTrackCreateView,
    PlaylistTrackDeleteView,
)


urlpatterns = [
    path('tracks/', TrackListView.as_view(), name='track-list'),
    path('tracks/<str:track_id>/', TrackDetailView.as_view(), name='track-detail'),
    path('analytics/popularity-distribution/', PopularityDistributionView.as_view(), name='popularity-distribution'),
    path('analytics/top-tracks/', TopTracksView.as_view(), name='top-tracks'),
    path('analytics/genre-popularity/', GenrePopularityView.as_view(), name='genre-popularity'),
    path('analytics/genre-energy-danceability/', GenreEnergyDanceabilityView.as_view(), name='genre-energy-danceability'),
    path('playlists/', PlaylistListCreateView.as_view(), name='playlist-list-create'),
    path('playlists/<int:pk>/', PlaylistDetailView.as_view(), name='playlist-detail'),
    path('playlists/add-track/', PlaylistTrackCreateView.as_view(), name='playlist-add-track'),
    path('playlists/remove-track/<int:pk>/', PlaylistTrackDeleteView.as_view(), name='playlist-remove-track'),
]