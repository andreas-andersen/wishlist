from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import (
    CustomUserCreationForm, 
    CustomUserChangeForm,
    CustomGroupAdminForm,
)
from .models import CustomGroup, CustomUser
from django.contrib.auth.models import Group

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username', 'assigned_to', 'responsible_by', 'is_leader',]

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password',)}),
        (None, {'fields': ('first_name', 'last_name',)}),
        (None, {'fields': ('assigned_to', 'responsible_by', 'is_leader')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'password1', 'password2', 
                'assigned_to', 'responsible_by',
                'assigned_to', 'responsible_by', 
                'is_leader',
            )
        }),
    )

class CustomGroupAdmin(admin.ModelAdmin):
    form = CustomGroupAdminForm
    model = CustomGroup
    filter_horizontal = ['permissions',]
    list_display = ['name', 'leader', 'created', 'deadline',]

admin.site.unregister(Group)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(CustomGroup, CustomGroupAdmin)