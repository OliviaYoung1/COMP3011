from django.db import models

#Created by Secure Copilot using the Spotify Tracks kaggle dataset: https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset
class Track(models.Model):
    track_id = models.CharField(max_length=50, primary_key=True)
    track_name = models.CharField(max_length=200)
    artists = models.CharField(max_length=500)
    album_name = models.CharField(max_length=200)
    popularity = models.IntegerField()
    duration_ms = models.IntegerField()
    explicit = models.BooleanField()
    danceability = models.FloatField()
    energy = models.FloatField()
    key = models.IntegerField()
    loudness = models.FloatField()
    mode = models.IntegerField()
    speechiness = models.FloatField()
    acousticness = models.FloatField()
    instrumentalness = models.FloatField()
    liveness = models.FloatField()
    valence = models.FloatField()
    tempo = models.FloatField()
    time_signature = models.IntegerField()
    track_genre = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.track_name} by {self.artists}"

