from django.db import models
from django.conf import settings
from cards.models import Card
# Create your models here.


class Card_collection(models.Model):
    title=models.CharField(max_length=100)
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cards=models.ManyToManyField(Card,related_name='collections')
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_collection')
    