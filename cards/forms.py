from django import forms
from cards.models import Card, Comment
from movies.models import Movie

class CardForm(forms.ModelForm):
    class Meta:
        model=Card
        exclude=('user', 'like_users','movie','movie_posterpath','collection')

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        exclude = ('card', 'user','like_users')