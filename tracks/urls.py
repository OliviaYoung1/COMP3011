from django.urls import path
from .views import TrackListView, TrackDetailView, PopularityDistributionView

urlpatterns = [
    path('tracks/', TrackListView.as_view(), name='track-list'),
    path('tracks/<str:track_id>/', TrackDetailView.as_view(), name='track-detail'),
    path('analytics/popularity-distribution/', PopularityDistributionView.as_view(), name='popularity-distribution'),
]