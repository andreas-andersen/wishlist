from django import forms
from django.db import models
from django.contrib.auth.forms import (
    UserCreationForm, 
    UserChangeForm,
)
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ['email', 'first_name', 'last_name']

class CustomUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm):
        model = CustomUser
        fields = UserChangeForm.Meta.fields

class UserActivationForm(forms.Form):
    first_name = forms.CharField(
        max_length=40,
        widget=forms.TextInput(attrs={'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        max_length=40,
        widget=forms.TextInput(attrs={'placeholder': 'Last Name'})
    )
    password1 = forms.CharField(
        max_length=20,
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )
    password2 = forms.CharField(
        max_length=20,
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'})
    )