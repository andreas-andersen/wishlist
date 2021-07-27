from django.contrib import admin
from django.contrib.auth.models import Group
from .forms import (
    CustomGroupAdminForm,
    AssignmentAdminForm,
    AssignmentsAdminForm,
)
from .models import (
    CustomGroup,
    Assignment,
    Assignments,
)

class CustomGroupAdmin(admin.ModelAdmin):
    form = CustomGroupAdminForm
    model = CustomGroup
    filter_horizontal = ['permissions',]
    list_display = ['name', 'leader', 'created', 'deadline',]

class AssignmentAdmin(admin.ModelAdmin):
    form = AssignmentAdminForm
    model = Assignment
    list_display = ['member', 'assignment']

class AssignmentsAdmin(admin.ModelAdmin):
    form = AssignmentsAdminForm
    model = Assignments
    list_display = ['group', 'time']

admin.site.unregister(Group)
admin.site.register(CustomGroup, CustomGroupAdmin)
admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(Assignments, AssignmentsAdmin)