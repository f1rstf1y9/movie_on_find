from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from movies.models import Movie


# Create your models here.
class Review(models.Model):
    STAR_CHOICES = [
        ('10',"★★★★★★★★★★"),
        ('9',"★★★★★★★★★"),
        ('8',"★★★★★★★★"),
        ('7',"★★★★★★★"),
        ('6',"★★★★★★"),
        ('5',"★★★★★"),
        ('4',"★★★★"),
        ('3',"★★★"),
        ('2',"★★"),
        ('1',"★"),
        (None, '선택')
    ]
    vote=models.CharField(max_length=10, choices=STAR_CHOICES)
    #스포일러추가
    spoiler=models.TextField()
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_reivew')
    movie=models.ForeignKey(Movie, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='review_comment')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_review_comment')

    def __str__(self):
        return self.content