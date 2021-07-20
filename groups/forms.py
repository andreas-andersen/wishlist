from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.core.exceptions import ValidationError
from accounts.models import CustomUser
from .models import CustomGroup

class CustomGroupAdminForm(forms.ModelForm):

    users = forms.ModelMultipleChoiceField(
        queryset=CustomUser.objects.all(), 
        required=False,
        widget=FilteredSelectMultiple('users', False)
    )
    invited_users = forms.ModelMultipleChoiceField(
        queryset=CustomUser.objects.all(), 
        required=False,
        widget=FilteredSelectMultiple('invited_users', False)
    )
    leader = forms.ModelChoiceField(
        queryset=CustomUser.objects.all(),
        to_field_name='email'
    )
    DKK = 'DKK'
    NOK = 'NOK'
    JPY = '¥'
    USD = "$"
    currency_choices = [
        (DKK, 'DKK'),
        (NOK, 'NOK'),
        (JPY, '¥'),
        (USD, '$'),
    ]
    currency = forms.ChoiceField(
        choices=currency_choices,
        required=False
    )

    def __init__(self, *args, **kwargs):
        super(CustomGroupAdminForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['users'].initial = self.instance.user_set.all()
            self.fields['invited_users'].initial = self.instance.invited_users.all()
            self.initial['leader'] = self.instance.leader
            self.fields['invited_users'].queryset = (
                CustomUser.objects.all().difference(self.instance.user_set.all())
            )

    def save_m2m(self):
        self.instance.user_set.set(self.cleaned_data['users'])
        self.instance.invited_users.set(self.cleaned_data['invited_users'])

    def save(self, *args, **kwargs):
        instance = super(CustomGroupAdminForm, self).save()
        self.save_m2m()
        return instance

    class Meta:
        model = CustomGroup
        exclude = []


class GroupMemberCreateForm(forms.Form):
    first_name = forms.CharField(
        max_length=40,
        widget=forms.TextInput(attrs={'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        max_length=40,
        widget=forms.TextInput(attrs={'placeholder': 'Last Name'})
    )


class GroupMemberInviteForm(forms.Form):
    email = forms.EmailField(
        max_length=50,
        widget=forms.EmailInput(attrs={'placeholder': 'email@address.com'})
    )
