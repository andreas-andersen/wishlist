#wishlist/views.py
from django.views.generic import ListView
from .models import Wish

class WishListView(ListView):
    model = Wish
    template_name = 'home.html'