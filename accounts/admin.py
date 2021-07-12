from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username', 'assigned_to', 'responsible_by', 'is_staff',]

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        (None, {'fields': ('assigned_to', 'responsible_by',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'assigned_to', 'responsible_by',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)