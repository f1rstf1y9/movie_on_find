from django import forms
from card_collections.models import Card_collection
from cards.models import Card

class CollectionForm(forms.ModelForm):
    class Meta:
        model=Card_collection
        exclude=('user','like_users','collection_color',)
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cards'].queryset = Card.objects.filter(user=user)