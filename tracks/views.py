from django.shortcuts import render
# tracks/views.py
from rest_framework import generics, filters
from .models import Track, Playlist, PlaylistTrack
from .serializers import TrackSerializer, PlaylistSerializer, PlaylistTrackSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Avg, Min, Max, Count

class PlaylistListCreateView(generics.ListCreateAPIView):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer

class PlaylistDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer

class PlaylistTrackCreateView(generics.CreateAPIView):
    queryset = PlaylistTrack.objects.all()
    serializer_class = PlaylistTrackSerializer

class PlaylistTrackDeleteView(generics.DestroyAPIView):
    queryset = PlaylistTrack.objects.all()
    serializer_class = PlaylistTrackSerializer

class TrackDetailView(generics.RetrieveAPIView):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    lookup_field = 'track_id'

class TrackListView(generics.ListAPIView):
    serializer_class = TrackSerializer

    def get_queryset(self):
        qs = Track.objects.all()
        params = self.request.query_params

        # --- SEARCH FOR TRACKS  ---
        search = params.get('search')
        if search:
            return (
                Track.objects
                .filter(track_name__icontains=search)
                .order_by('-popularity')[:5]
            )

        artist = params.get('artist')
        genre = params.get('genre')
        track_name = params.get('track_name')

        min_pop = params.get('min_popularity')
        max_pop = params.get('max_popularity')
        min_tempo = params.get('min_tempo')
        max_tempo = params.get('max_tempo')

        explicit = params.get('explicit')

        if artist:
            qs = qs.filter(artists__icontains=artist)
        if genre:
            qs = qs.filter(track_genre__icontains=genre)
        if track_name:
            qs = qs.filter(track_name__icontains=track_name)

        if min_pop:
            qs = qs.filter(popularity__gte=min_pop)
        if max_pop:
            qs = qs.filter(popularity__lte=max_pop)

        if min_tempo:
            qs = qs.filter(tempo__gte=min_tempo)
        if max_tempo:
            qs = qs.filter(tempo__lte=max_tempo)

        if explicit in ['true', 'false']:
            qs = qs.filter(explicit=(explicit == 'true'))

        order = params.get('order_by')
        if order:
            qs = qs.order_by(order)

        return qs

class TopTracksView(APIView):
    def get(self, request):
        qs = Track.objects.all()
        p = request.query_params

        # --- numeric filters ---
        def apply_num(param, field, cast):
            val = p.get(param)
            if val:
                try:
                    return {field: cast(val)}
                except ValueError:
                    return {}
            return {}

        num_map = [
            ('min_popularity', 'popularity__gte', int),
            ('max_popularity', 'popularity__lte', int),
            ('min_danceability', 'danceability__gte', float),
            ('max_danceability', 'danceability__lte', float),
            ('min_energy', 'energy__gte', float),
            ('max_energy', 'energy__lte', float),
            ('min_valence', 'valence__gte', float),
            ('max_valence', 'valence__lte', float),
            ('min_tempo', 'tempo__gte', float),
            ('max_tempo', 'tempo__lte', float),
        ]

        for param, field, cast in num_map:
            filt = apply_num(param, field, cast)
            if filt:
                qs = qs.filter(**filt)

        # --- text filters ---
        if p.get('genre'):
            qs = qs.filter(track_genre__icontains=p['genre'])
        if p.get('artist'):
            qs = qs.filter(artists__icontains=p['artist'])
        if p.get('track_name'):
            qs = qs.filter(track_name__icontains=p['track_name'])

        # --- explicit filter ---
        explicit = p.get('explicit')
        if explicit in ['true', 'false']:
            qs = qs.filter(explicit=(explicit == 'true'))

        # --- ordering + limit ---
        qs = qs.order_by('-popularity')

        limit = p.get('limit')
        try:
            limit = int(limit) if limit else 10
        except ValueError:
            limit = 10

        qs = qs[:limit]

        serializer = TrackSerializer(qs, many=True)
        return Response({
            "limit": limit,
            "results": serializer.data
        })
    
class PopularityDistributionView(APIView):
    def get(self, request):
        qs = Track.objects.all()

        # Summary statistics
        summary = qs.aggregate(
            mean=Avg('popularity'),
            min=Min('popularity'),
            max=Max('popularity')
        )

        # Median (manual because SQLite has no built-in median)
        values = list(qs.values_list('popularity', flat=True))
        values.sort()
        n = len(values)
        median = values[n // 2] if n % 2 == 1 else (values[n // 2 - 1] + values[n // 2]) / 2

        # Buckets
        buckets = [
            {"range": "0-20", "count": qs.filter(popularity__gte=0, popularity__lt=20).count()},
            {"range": "20-40", "count": qs.filter(popularity__gte=20, popularity__lt=40).count()},
            {"range": "40-60", "count": qs.filter(popularity__gte=40, popularity__lt=60).count()},
            {"range": "60-80", "count": qs.filter(popularity__gte=60, popularity__lt=80).count()},
            {"range": "80-100", "count": qs.filter(popularity__gte=80, popularity__lte=100).count()},
        ]

        return Response({
            "summary": {
                "mean": summary["mean"],
                "median": median,
                "min": summary["min"],
                "max": summary["max"]
            },
            "buckets": buckets
        })

class GenrePopularityView(APIView):
    def get(self, request):
        params = request.query_params

        # Minimum number of tracks required for a genre to appear
        min_tracks = params.get('min_tracks')
        try:
            min_tracks = int(min_tracks) if min_tracks else 1
        except ValueError:
            min_tracks = 1

        # Base aggregation
        qs = (
            Track.objects
            .values('track_genre')
            .annotate(
                avg_popularity=Avg('popularity'),
                avg_energy=Avg('energy'),
                avg_danceability=Avg('danceability'),
                avg_valence=Avg('valence'),
                track_count=Count('track_id')
            )
            .filter(track_count__gte=min_tracks)
        )

        # Optional ordering
        order = params.get('order_by')
        if order:
            qs = qs.order_by(order)

        return Response({"results": list(qs)})

class GenreEnergyDanceabilityView(APIView):
    def get(self, request):
        params = request.query_params

        # Minimum number of tracks required for a genre to appear
        min_tracks = params.get('min_tracks')
        try:
            min_tracks = int(min_tracks) if min_tracks else 1
        except ValueError:
            min_tracks = 1

        # Base aggregation
        qs = (
            Track.objects
            .values('track_genre')
            .annotate(
                avg_energy=Avg('energy'),
                avg_danceability=Avg('danceability'),
                avg_valence=Avg('valence'),
                avg_tempo=Avg('tempo'),
                track_count=Count('track_id')
            )
            .filter(track_count__gte=min_tracks)
        )

        # ordering
        order = params.get('order_by')
        if order:
            qs = qs.order_by(order)

        return Response({"results": list(qs)})
    
class GenreListView(APIView):
    def get(self, request):
        genres = (
            Track.objects
            .values_list('track_genre', flat=True)
            .distinct()
            .order_by('track_genre')
        )
        return Response({"genres": list(genres)})
