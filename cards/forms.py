from django import forms
from cards.models import Card, Comment
from movies.models import Movie

class CardForm(forms.ModelForm):
    # movies = forms.ModelChoiceField(Movie.objects.values('title'), initial=None)
    class Meta:
        model=Card
        exclude=('user', 'like_users', 'movie',)

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        exclude = ('card', 'user','like_users')