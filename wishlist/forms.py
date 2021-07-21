from django import forms
from django.forms import ModelForm
from django.forms.widgets import TextInput
from .models import Wish
from accounts.models import CustomUser

class WishCreateForm(ModelForm):
    title = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Item name',
                'class': 'in-page-input'}))
    HIGH_PRIORITY = 'HI'
    MEDIUM_PRIORITY = 'MD'
    LOW_PRIORITY = 'LO'
    priority_choices = [
        ('', 'Priority'),
        (HIGH_PRIORITY, "High"),
        (MEDIUM_PRIORITY, "Medium"),
        (LOW_PRIORITY, "Low"),
    ]
    priority = forms.ChoiceField(
        choices=priority_choices,
        required=False,
        #default=HIGH_PRIORITY,
        widget=forms.Select(
            attrs={
                'placeholder': 'Priority',
                'class': 'in-page-input'}))
    details = forms.CharField(
        max_length=200,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Details: e.g. color, size, brand, etc.',
                'class': 'in-page-input'}))

    class Meta:
        model = Wish
        fields = ['title', 'priority', 'details']