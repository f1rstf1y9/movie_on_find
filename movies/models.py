from django.db import models
from django.conf import settings

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name
class Actor(models.Model):
    name=models.CharField(max_length=100)
class Movie(models.Model):
    title = models.CharField(max_length=100)
    vote_average = models.FloatField(null=True, blank=True)
    overview = models.TextField(null=True, blank=True)
    poster_path = models.CharField(max_length=500, null=True, blank=True)
    genres = models.ManyToManyField(Genre, related_name= 'movies')
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_movies')
    wish_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='wish_movies')

class Comment(models.Model):
    movie = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content=models.CharField(max_length=200)
    vote=models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)