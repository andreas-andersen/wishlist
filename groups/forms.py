from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from accounts.models import CustomUser
from .models import (
    CustomGroup,
    Assignment,
    Assignments,
)

class CustomGroupAdminForm(forms.ModelForm):
    users = forms.ModelMultipleChoiceField(
        queryset=CustomUser.objects.all(), 
        required=False,
        widget=FilteredSelectMultiple('users', False))
    invited_users = forms.ModelMultipleChoiceField(
        queryset=CustomUser.objects.all(), 
        required=False,
        widget=FilteredSelectMultiple('invited_users', False))
    leader = forms.ModelChoiceField(
        queryset=CustomUser.objects.all(),
        to_field_name='email')
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
        required=False)

    def __init__(self, *args, **kwargs):
        super(CustomGroupAdminForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['users'].initial = self.instance.user_set.all()
            self.fields['invited_users'].initial = self.instance.invited_users.all()
            self.initial['leader'] = self.instance.leader
            self.fields['invited_users'].queryset = (
                CustomUser.objects.all().difference(self.instance.user_set.all()))

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

class AssignmentAdminForm(forms.ModelForm):
    member = forms.ModelChoiceField(
        queryset=CustomUser.objects.all(), 
        required=True)
    assignment = forms.ModelChoiceField(
        queryset=CustomUser.objects.all(), 
        required=True)

    class Meta:
        model = Assignment
        exclude = []

class AssignmentsAdminForm(forms.ModelForm):
    group = forms.ModelChoiceField(
        queryset=CustomGroup.objects.all(),
        required=True)
    assignments = forms.ModelMultipleChoiceField(
        queryset=Assignment.objects.all(), 
        required=False,
        widget=FilteredSelectMultiple('assignments', False))

    def __init__(self, *args, **kwargs):
        super(AssignmentsAdminForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['assignments'].initial = self.instance.assignments.all()

    def save_m2m(self):
        self.instance.assignments.set(self.cleaned_data['assignments'])

    def save(self, *args, **kwargs):
        instance = super(AssignmentsAdminForm, self).save()
        self.save_m2m()
        return instance

    class Meta:
        model = Assignments
        exclude = []


class GroupCreateForm(forms.ModelForm):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Group Name',
                'class': 'form-page-input',
                'autofocus': 'autofocus'}))
    max_gift_value = forms.DecimalField(
        max_digits=20,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(
            attrs={
                'placeholder': 'Maximum Gift Value',
                'class': 'form-page-input'
            }
        )
    )
    DKK = 'DKK'
    NOK = 'NOK'
    JPY = '¥'
    USD = "$"
    currency_choices = [
        ('', 'Currency'),
        (DKK, 'DKK'),
        (NOK, 'NOK'),
        (JPY, '¥'),
        (USD, '$'),
    ]
    currency = forms.ChoiceField(
        choices=currency_choices,
        required=False,
        widget=forms.Select(
            attrs={
                'class': 'form-page-input'}))
    deadline = forms.DateField(
        required=True,
        widget=forms.DateInput(
            attrs={
                'placeholder': 'DD/MM/YYYY',
                'class': 'form-page-input',
                'autocomplete': 'off'}))

    class Meta:
        model = CustomGroup
        fields = ['name', 'max_gift_value', 'currency', 'deadline',]


class GroupMemberCreateForm(forms.Form):
    first_name = forms.CharField(
        max_length=40,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'First Name',
                'class': 'in-page-input'})
    )
    last_name = forms.CharField(
        max_length=40,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Last Name',
                'class': 'in-page-input'})
    )


class GroupMemberInviteForm(forms.Form):
    email = forms.EmailField(
        max_length=50,
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'email@address.com',
                'class': 'in-page-input'}))


class ManualAssignmentForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.current_group = kwargs.pop('group')
        self.group_members = self.current_group.user_set.all()
        self.selector_choices = [(user.id, user.first_name + ' ' + user.last_name) for user in self.group_members]
        self.selector_choices.insert(0, ('', 'Assigned to'))
        super(ManualAssignmentForm, self).__init__(*args, **kwargs)

        for i, member in enumerate(self.group_members):
            field_name = f'assignment_{member.id}'
            current_selection = self.selector_choices.copy()
            current_selection.pop(i+1)
            self.fields[field_name] = forms.ChoiceField(
                label=f'{member.first_name} {member.last_name}',
                choices=current_selection,
                required=True,
                widget=forms.Select(
                    attrs={
                        'class': 'form-page-input'}))

    def clean(self):
        assignments = list()
        
        for member in self.group_members:
            field_name = f'assignment_{member.id}'
            self.cleaned_data.get(field_name)
            assignment = self.cleaned_data[field_name]
            if assignment in assignments:
                self.add_error(field_name, 'This member is assigned multiple times')
            else:
                assignments.append((field_name, assignment))

        self.cleaned_data['assignments'] = assignments