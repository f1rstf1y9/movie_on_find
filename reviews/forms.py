from django import forms
from reviews.models import Review,Comment
from movies.models import Movie

class ReviewForm(forms.ModelForm):
    # movies = forms.ModelChoiceField(Movie.objects.values('title'), initial=None)
    class Meta:
        model=Review
        exclude=('user', 'like_users','movie','spoiler')

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        exclude = ('review', 'user','like_users')