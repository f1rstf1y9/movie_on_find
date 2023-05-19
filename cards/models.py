from django.db import models
from django.conf import settings


# Create your models here.
# class Board(models.Model):
#     author=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     title = models.CharField(max_length=100)
#     content = models.TextField()
#     like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_boards')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

# class Comment(models.Model):
#     author=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     board = models.ForeignKey(Board, on_delete=models.CASCADE)
#     content = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)