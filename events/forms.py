from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class EventForm(forms.ModelForm):
    date = forms.DateTimeField(widget=forms.DateTimeInput(
        attrs={
            'type': 'datetime-local',
            'class': 'form-control'
        }
    ),
        label='Дата и время',
        input_formats=['%Y-%m-%dT%H:%M']
    )
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label='Категории'
    )

    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'location', 'categories', 'headline_image', 'participant_limit']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
