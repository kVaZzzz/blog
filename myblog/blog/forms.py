from django import forms
from django.contrib.auth.hashers import make_password
from .models import *


class UserForm(forms.ModelForm):

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data["password"]
        if password:
            user.password = make_password(password)
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ['name', 'surname', 'username', 'email', 'password', 'avatar']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['name', 'content', 'photo']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'photo']


class CommentCommentForm(forms.ModelForm):
    class Meta:
        model = CommentCommented
        fields = ['content', 'photo']
