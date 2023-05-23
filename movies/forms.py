from django import forms
# from movies.models import Comment


class Searchform(forms.Form):
    keyword=forms.CharField(max_length=100,required=False,widget=forms.TextInput(attrs={'placeholder': '검색어를 입력하세요'}))
    