from django import forms
from .models import Profile, Feedback
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
        ]
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'password1': forms.PasswordInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'password2': forms.PasswordInput(
                attrs={
                    'class': 'form-control'
                }
            ),
        }


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['rating', 'review']
        widgets = {
            'rating': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'review': forms.Textarea(
                attrs={
                    'class': 'form-control'
                }
            )
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture']
        widgets = {
            'profile_picture': forms.FileInput(
                attrs={
                    'style': 'display: none;',
                }
            )
        }