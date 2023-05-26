from django import forms
from cards.models import Card
from movies.models import Movie
from .widgets import DatePickerInput

class CardForm(forms.ModelForm):
    # movies = forms.ModelChoiceField(Movie.objects.values('title'), initial=None)
    class Meta:
        model=Card
        exclude=('user', 'like_users', 'movie',)

        watched_date = forms.DateField(widget=DatePickerInput)
        widgets = {
            'watched_date': DatePickerInput(),
        }