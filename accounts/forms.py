from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import User

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('email', 'profile_image', 'nickname', 'kakao_id', 'like_genres')

        widgets={
            'nickname': forms.Textarea(attrs={"rows":"1"}),
            'like_genres' : forms.CheckboxSelectMultiple()
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        
        if commit:
            user.save()
        user.like_genres.set(self.cleaned_data["like_genres"])
        return user

class UserChangeForm(forms.ModelForm):
    email = forms.CharField(disabled=True)

    class Meta:
        model = User
        fields = ('email', 'profile_image', 'nickname', 'like_genres',)
        widgets={
            'nickname': forms.Textarea(attrs={"rows":"1"}),
            'like_genres' : forms.CheckboxSelectMultiple()
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.profile_image = self.cleaned_data["profile_image"]

        if commit:
            user.save()
        user.like_genres.set(self.cleaned_data["like_genres"])
        return user
