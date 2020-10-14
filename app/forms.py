from django import forms
from app.models import Profile, Question, Tag, Answer
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


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


class QuestionForm(forms.ModelForm):
    tags_field = forms.CharField()

    class Meta:
        model = Question
        fields = ['title', 'content', 'tags_field']

    def __init__(self, profile, *args, **kwargs):
        self.author = profile
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        obj = super().save(commit=False)
        obj.author = self.author
        if commit:
            obj.save()
            for tag in self.cleaned_data['tags_field'].split(' '):
                try:
                    Tag.objects.get(name=tag)
                except Tag.DoesNotExist:
                    Tag.objects.create(name=tag)
                obj.tags.add(Tag.objects.get(name=tag))
            obj.save()
        return obj


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']

    def __init__(self, profile, question, *args, **kwargs):
        self.author = profile
        self.question = question
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        obj = super().save(commit=False)
        obj.author = self.author
        obj.question = self.question
        if commit:
            obj.save()
        return obj
