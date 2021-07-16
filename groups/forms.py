from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.db.models.query import QuerySet
from accounts.models import CustomUser
from .models import CustomGroup

class CustomGroupAdminForm(forms.ModelForm):

    users = forms.ModelMultipleChoiceField(
         queryset=CustomUser.objects.all(), 
         required=False,
         widget=FilteredSelectMultiple('users', False)
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

    def save_m2m(self):
        self.instance.user_set.set(self.cleaned_data['users'])

    def save(self, *args, **kwargs):
        instance = super(CustomGroupAdminForm, self).save()
        self.save_m2m()
        return instance

    class Meta:
        model = CustomGroup
        exclude = []


class GroupMemberCreateForm(forms.ModelForm):

    is_self_responsible = forms.BooleanField(
        required=False
    )
    
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'is_self_responsible', 'responsible_by']

    def __init__(self, *args, **kwargs):
        self.group = kwargs.pop('group', None)
        super(GroupMemberCreateForm, self).__init__(*args, **kwargs)
        if self.group:
            self.fields['responsible_by'].queryset = self.group.user_set.all().filter(is_self_responsible=True)
