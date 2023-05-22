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
    video = models.TextField(null=True, blank=True)
    genres = models.ManyToManyField(Genre, related_name= 'movies')
    # watching,interest,watched
    interest = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='interest_movies')
    watching = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='watching_movies')
    watched = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='watched_movies')

# class Comment(models.Model):
#     STAR_CHOICES = [
#         ('10',"★★★★★★★★★★"),
#         ('9',"★★★★★★★★★"),
#         ('8',"★★★★★★★★"),
#         ('7',"★★★★★★★"),
#         ('6',"★★★★★★"),
#         ('5',"★★★★★"),
#         ('4',"★★★★"),
#         ('3',"★★★"),
#         ('2',"★★"),
#         ('1',"★"),
#         (None, '선택')
#     ]
#     movie=models.ForeignKey(Movie, on_delete=models.CASCADE)
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     content=models.CharField(max_length=200)
#     vote=models.CharField(max_length=10, choices=STAR_CHOICES)
#     #스포일러추가
#     spoiler=models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)