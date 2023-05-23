from django.db import models
from django.conf import settings
from movies.models import Movie
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
class Card(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.CharField(max_length=20)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_cards')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    card_image = models.ImageField()
    movie_type = models.CharField(max_length=5, choices=[('2D', '2D'), ('3D', '3D'), ('4D', '4D'),])
    movie_location = models.CharField(max_length=10, choices=[('방구석 1열', '방구석 1열'), ('영화관', '영화관'),])
    watched_at = models.DateField()
    watched_people = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(10)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)