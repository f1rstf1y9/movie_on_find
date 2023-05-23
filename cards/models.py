from django.db import models
from django.conf import settings
from movies.models import Movie


# Create your models here.
class Card(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    card_image = models.ImageField()
    content = models.TextField()
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_cards')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    movie_type = models.CharField(max_length=5, choices=[('2D', '2D'), ('3D', '3D'), ('4D', '4D'),])
    watched_location = models.CharField(max_length=10, choices=[('안방 1열', '안방 1열'), ('영화관', '영화관')])
    watched_people = models.IntegerField()
    watched_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)