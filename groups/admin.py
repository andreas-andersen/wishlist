from django.contrib import admin
from django.contrib.auth.models import Group
from .forms import CustomGroupAdminForm
from .models import CustomGroup


class CustomGroupAdmin(admin.ModelAdmin):
    form = CustomGroupAdminForm
    model = CustomGroup
    filter_horizontal = ['permissions',]
    list_display = ['name', 'leader', 'created', 'deadline',]

admin.site.unregister(Group)
admin.site.register(CustomGroup, CustomGroupAdmin)