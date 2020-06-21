from django import forms
from app.models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import urllib


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email']

    def clean_username(self):
        username = self.cleaned_data['username']
        if ' ' in username:
            self.add_error('username', 'Username contains whitespace.')
        return username

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):
    avatar = forms.ImageField(required=False)

    class Meta:
        model = Profile
        fields = ['avatar']
