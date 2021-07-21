from django import forms
from django.db import models
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import (
    AuthenticationForm,
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

class CustomUserSignupForm(UserCreationForm):
    email = forms.CharField(
        max_length=40,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Email',
                'class': 'form-page-input'}))
    first_name = forms.CharField(
        max_length=40,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'First Name',
                'class': 'form-page-input'}))
    last_name = forms.CharField(
        max_length=40,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Last Name',
                'class': 'form-page-input'}))
    password1 = forms.CharField(
        max_length=40,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Password',
                'class': 'form-page-input'}))
    password2 = forms.CharField(
        max_length=40,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Repeat Password',
                'class': 'form-page-input'}))

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2']

class CustomUserLoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=40,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Email',
                'class': 'form-page-input'}))
    password = forms.CharField(
        max_length=40,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Password',
                'class': 'form-page-input'}))

    class Meta:
        model = CustomUser
        fields = ['username','password']

    def __init__(self, *args, **kwargs):
        super(CustomUserLoginForm, self).__init__(*args, **kwargs)

class CustomUserActivationForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=40,
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'First Name',
                'class': 'form-page-input'}))
    last_name = forms.CharField(
        max_length=40,
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Last Name',
                'class': 'form-page-input'}))
    password1 = forms.CharField(
        max_length=40,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Password',
                'class': 'form-page-input'}))
    password2 = forms.CharField(
        max_length=40,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Repeat Password',
                'class': 'form-page-input'}))

    class Meta:
        model = CustomUser
        fields = ['first_name','last_name','password1','password2']

    def clean(self):
        cleaned_data = super(CustomUserActivationForm, self).clean()
        password1 = cleaned_data['password1']
        password2 = cleaned_data['password2']

        try:
            validate_password(password1, self.instance)
        except ValidationError as error:
            self.add_error('password2', error)

        if password1 != password2:
            raise ValidationError('The two passwords do not match')
    
    """ def clean_password1(self):
                password = self.cleaned_data.get('password1')
                if password:
                    try:
                        validate_password(password, self.instance)
                    except ValidationError as error:
                        self.add_error('password1', error)
                        
    def clean_password2(self):
        password = self.cleaned_data.get('password1')
        if password:
            try:
                validate_password(password, self.instance)
            except ValidationError as error:
                self.add_error('password1', error) """