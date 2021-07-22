from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordResetForm,
    SetPasswordForm,
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

class CustomUserPasswordChangeForm(SetPasswordForm):

    new_password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Enter new password',
                'class': 'in-page-input',
                'autofocus': 'autofocus'}))
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Repeat password',
                'class': 'in-page-input',
                'autofocus': 'autofocus'}))

    class Meta:
        model= CustomUser
        fields = ['new_password1', 'new_password2']

class CustomUserSignupForm(UserCreationForm):
    email = forms.CharField(
        max_length=40,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Email',
                'class': 'form-page-input',
                'autofocus': 'autofocus'}))
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
                'class': 'form-page-input',
                'autofocus': 'autofocus'}))
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
                'class': 'form-page-input',
                'autofocus': 'autofocus'}))
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