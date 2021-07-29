from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import (
    CustomUserCreationForm, 
    CustomUserChangeForm,
    NotificationAdminForm,
)
from .models import CustomUser, Notification


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    ordering = ('-date_joined',)
    list_display = [
        'email', 'first_name', 'last_name', 
        'assigned_to', 'responsible_by', 
        'is_leader', 'is_self_responsible',
    ]
    list_filter = ['is_active','groups',]

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
                'first_name', 'last_name',
                'assigned_to', 'responsible_by',
                'is_leader', 'is_self_responsible',
            )
        }),
    )

class NotificationAdmin(admin.ModelAdmin):
    form = NotificationAdminForm
    model = Notification
    list_display = ['user', 'content', 'read']


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Notification, NotificationAdmin)