#wishlist/views.py
from django.views.generic import ListView, DetailView
from django.views.generic.edit import (
    CreateView, UpdateView, DeleteView
)
from django.urls import reverse_lazy
from .models import Wish

class WishListView(ListView):
    model = Wish
    context_object_name = 'wish'
    template_name = 'home.html'

class WishDetailView(DetailView):
    model = Wish
    context_object_name = 'wish'
    template_name = 'wish_detail.html'

class WishCreateView(CreateView):
    model = Wish
    context_object_name = 'wish'
    template_name = 'wish_new.html'
    fields = ['title', 'author', 'priority', 'details']

class WishUpdateView(UpdateView):
    model = Wish
    context_object_name = 'wish'
    template_name = 'wish_update.html'
    fields = ['title', 'priority', 'details']

class WishDeleteView(DeleteView):
    model = Wish
    context_object_name = 'wish'
    template_name = 'wish_delete.html'
    success_url = reverse_lazy('home')