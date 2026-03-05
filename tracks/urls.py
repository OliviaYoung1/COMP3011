from django.urls import path
from .views import (
    TrackListView,
    TrackDetailView,
    PopularityDistributionView,
    TopTracksView
)


urlpatterns = [
    path('tracks/', TrackListView.as_view(), name='track-list'),
    path('tracks/<str:track_id>/', TrackDetailView.as_view(), name='track-detail'),
    path('analytics/popularity-distribution/', PopularityDistributionView.as_view(), name='popularity-distribution'),
    path('analytics/top-tracks/', TopTracksView.as_view(), name='top-tracks'),
]