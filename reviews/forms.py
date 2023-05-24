from django import forms
from reviews.models import Review,Comment
from movies.models import Movie

class ReviewForm(forms.ModelForm):
    # movies = forms.ModelChoiceField(Movie.objects.values('title'), initial=None)
    class Meta:
        model = Review
        spoiler = forms.BooleanField()
        exclude = ('user', 'like_users','movie',)

class CommentForm(forms.ModelForm):
    content = forms.CharField(label='content', widget=forms.Textarea(attrs={'placeholder': '해당 리뷰에 대한 의견을 남겨보세요!'}))
    class Meta:
        model = Comment
        exclude = ('review', 'user','like_users')
        