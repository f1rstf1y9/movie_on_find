from django.db import models
from django.conf import settings

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=100)
    original_title = models.CharField(max_length=100)
    vote_average = models.FloatField(null=True, blank=True)
    overview = models.TextField(null=True, blank=True)
    popularity = models.TextField(null=True, blank=True)
    runtime=models.IntegerField(null=True, blank=True)
    release_date = models.CharField(max_length=500, null=True, blank=True)
    poster_path = models.CharField(max_length=500, null=True, blank=True)
    backdrop_path = models.CharField(max_length=500, null=True, blank=True)
    video = models.TextField(null=True, blank=True)
    genres = models.ManyToManyField(Genre, related_name= 'movies')
    # watching,interest,watched
    interest = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='interest_movies')
    watching = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='watching_movies')
    watched = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='watched_movies')

# class Actor(models.Model):
#     name=models.CharField(max_length=100)
    # movie=models.ManyToManyField(Movie, related_name='actor')