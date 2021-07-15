from django import forms
from django.forms import ModelForm
from .models import Wish
from accounts.models import CustomUser

class WishCreationForm(ModelForm):

    title = forms.CharField(max_length=100)
    author = forms.ModelChoiceField(
        queryset=CustomUser.objects.all(),
        to_field_name='username'
    )
    HIGH_PRIORITY = 'HI'
    MEDIUM_PRIORITY = 'MD'
    LOW_PRIORITY = 'LO'
    priority_choices = [
        (HIGH_PRIORITY, "High"),
        (MEDIUM_PRIORITY, "Medium"),
        (LOW_PRIORITY, "Low"),
    ]
    priority = forms.ChoiceField(choices=priority_choices)
    details = forms.CharField(
        required=False
    )

    class Meta:
        model = Wish
        fields = ['title', 'priority', 'details']