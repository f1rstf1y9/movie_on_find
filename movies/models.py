from django.db import models
from django.conf import settings

# Create your models here.
class Actor(models.Model):
    name=models.CharField(max_length=100)
    profile_path=models.TextField()
class Genre(models.Model):
    genres=models.TextField()
class Actor(models.Model):
    name=models.CharField(max_length=100)
class Movie(models.Model):
    title=models.CharField(max_length=100)
    overview = models.TextField()
    vote_average=models.TextField()
    poster_path=models.TextField()
    genre_ids=models.ManyToManyField(Genre)
    actors=models.ManyToManyField(Actor, related_name="actors")

class Comment(models.Model):
    movie=models.ManyToManyField(Movie)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content=models.TextField()