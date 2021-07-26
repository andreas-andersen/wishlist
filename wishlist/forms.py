from django import forms
from .models import Wish

class WishCreateForm(forms.ModelForm):
    title = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Item name',
                'class': 'in-page-input',
                'autofocus': 'autofocus'}))
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
    link = forms.URLField(
        required=False,
        widget=forms.URLInput(
            attrs={
                'placeholder': 'https://',
                'class': 'in-page-input'
            }))

    class Meta:
        model = Wish
        fields = ['title', 'priority', 'details', 'link']

class WishDetailedCreateForm(forms.ModelForm):
    title = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Item name',
                'class': 'form-page-input',
                'autofocus': 'autofocus'}))
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
        widget=forms.Select(
            attrs={
                'placeholder': 'Priority',
                'class': 'form-page-input'}))
    details = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Details: e.g. color, size, brand, etc.',
                'style': 'resize:none;',
                'class': 'form-page-input'}))
    link = forms.URLField(
        required=False,
        widget=forms.URLInput(
            attrs={
                'placeholder': 'https://',
                'class': 'form-page-input'
            }))

    class Meta:
        model = Wish
        fields = ['title', 'priority', 'details', 'link']

class WishUpdateForm(forms.ModelForm):
    title = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Item name',
                'class': 'form-page-input',
                'autofocus': 'autofocus'}))
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
        widget=forms.Select(
            attrs={
                'placeholder': 'Priority',
                'class': 'form-page-input'}))
    link = forms.URLField(
        required=False,
        widget=forms.URLInput(
            attrs={
                'placeholder': 'https://',
                'class': 'form-page-input',
                'onClick': 'this.setSelectionRange(0, this.value.length)',
            }))
    details = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Details: e.g. color, size, brand, etc.',
                'style': 'resize:none;',
                'class': 'form-page-input'}))

    class Meta:
        model = Wish
        fields = ['title', 'priority', 'link', 'details']

    def __init__(self, *args, **kwargs):
        super(WishUpdateForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.initial['title'] = self.instance.title
            self.initial['priority'] = self.instance.priority
            self.initial['details'] = self.instance.details