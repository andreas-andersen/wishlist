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


class GroupMemberCreateForm(forms.ModelForm):
    
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ['email', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super(GroupMemberCreateForm, self).__init__(*args, **kwargs)
        self.fields['email'].initial = str(CustomUser.objects.latest('id').pk + 1) + '@not-an-address.com'

class GroupMemberInviteForm(forms.ModelForm):

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'email@address.com'})
    )

    def __init__(self, *args, **kwargs):
        self.group_id = kwargs.pop('group_id', None)
        super(GroupMemberInviteForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            existing_user = CustomUser.objects.get(email=email)
            current_group = CustomGroup.objects.get(id=self.group_id)
            if existing_user not in current_group.user_set.all():
                if existing_user not in current_group.invited_users.all():
                    current_group.invited_users.add(existing_user)
                    raise ValidationError(f'User {email} already exists, invitation sent.')
                else:
                    raise ValidationError(f'User {email} already invited')
            else:
                raise ValidationError(f'User {email} is already a member of the group')
        return email
    
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ['email']
