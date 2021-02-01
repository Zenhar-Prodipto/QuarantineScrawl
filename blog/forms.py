from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post, Comment, Like


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["user_comment"]
