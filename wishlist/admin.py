from django.contrib import admin
from .models import Wish

class WishAdmin(admin.ModelAdmin):
    model = Wish
    list_display = ['title', 'author', 'group', 'priority',]

admin.site.register(Wish, WishAdmin)