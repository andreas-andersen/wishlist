from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import (
    CustomUserCreationForm, 
    CustomUserChangeForm,
)
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    ordering = ('-email',)
    list_display = [
        'email', 'first_name', 'last_name', 
        'assigned_to', 'responsible_by', 
        'is_leader', 'is_self_responsible',
    ]
    list_filter = ['groups',]

    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        (None, {'fields': ('first_name', 'last_name',)}),
        (None, {'fields': ('assigned_to', 'responsible_by', 'is_leader','is_self_responsible',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'password1', 'password2', 
                'assigned_to', 'responsible_by',
                'is_leader', 'is_self_responsible',
            )
        }),
    )


admin.site.register(CustomUser, CustomUserAdmin)