import pandas as pd
from .models import Track

def load():
    df = pd.read_csv("spotify.csv")

    for i, row in df.iterrows():
        Track.objects.update_or_create(
            track_id=row['track_id'],
            defaults={
                'track_name': row['track_name'],
                'artists': row['artists'],
                'album_name': row['album_name'],
                'popularity': row['popularity'],
                'duration_ms': row['duration_ms'],
                'explicit': row['explicit'],
                'danceability': row['danceability'],
                'energy': row['energy'],
                'key': row['key'],
                'loudness': row['loudness'],
                'mode': row['mode'],
                'speechiness': row['speechiness'],
                'acousticness': row['acousticness'],
                'instrumentalness': row['instrumentalness'],
                'liveness': row['liveness'],
                'valence': row['valence'],
                'tempo': row['tempo'],
                'time_signature': row['time_signature'],
                'track_genre': row['track_genre'],
            }
        )