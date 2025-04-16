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
        widgets = {
            'text': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                    'placeholder': 'Оставьте ваш комментарий...'
                }
            )
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text', 'rating']
        widgets = {
            'text': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                    'placeholder': 'Оставьте ваш отзыв...'
                }
            ),
            'rating': forms.Select(
                attrs={'class': 'form-control'},
                choices=[(i, i) for i in range(1, 6)]
            ),
        }
        labels = {
            'text': 'Отзыв',
            'rating': 'Оценка (от 1 до 5)',
        }


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('avatar', 'bio')