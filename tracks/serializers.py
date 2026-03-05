# tracks/serializers.py
from rest_framework import serializers
from .models import Track, Playlist, PlaylistTrack


class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = '__all__'


# Nested serializer: shows the Track details inside each PlaylistTrack
class PlaylistTrackDetailSerializer(serializers.ModelSerializer):
    track = TrackSerializer(read_only=True)

    class Meta:
        model = PlaylistTrack
        fields = ['id', 'track']


# Main Playlist serializer: now includes a "tracks" field
class PlaylistSerializer(serializers.ModelSerializer):
    tracks = PlaylistTrackDetailSerializer( many=True, read_only=True)

    class Meta:
        model = Playlist
        fields = ['id', 'name', 'description', 'created_at', 'tracks']


# Serializer used when adding a track to a playlist (POST /add-track/)
class PlaylistTrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaylistTrack
        fields = '__all__'