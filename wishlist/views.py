#wishlist/views.py
from accounts.models import CustomUser
from django.urls import reverse_lazy
from .models import Wish
from accounts.models import CustomUser
from django.views.generic import (
    ListView, 
    DetailView,
    TemplateView,
)
from django.views.generic.edit import (
    CreateView,
    UpdateView, 
    DeleteView,
)

class HomePageView(TemplateView):
    template_name='home.html'

class WishDetailView(DetailView):
    model = Wish
    context_object_name = 'wish'
    template_name = 'wish_detail.html'

class WishCreateView(CreateView):
    model = Wish
    context_object_name = 'wish'
    template_name = 'wish_new.html'
    fields = ('title', 'author', 'priority', 'details')

    def get_initial(self):
        return {'author': CustomUser.objects.get(id=self.kwargs['author_id'])}

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

class WishListView(ListView):
    model = Wish
    context_object_name = 'wish'
    template_name = 'wish_list.html'

    def possessive_ending(self, word):
        return word + "'" if word[-1] == 's' else word + "'s"

    def get_queryset(self):
        return Wish.objects.filter(author_id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        list_owner = CustomUser.objects.get(id=self.kwargs['pk'])
        data['list_owner_id'] = list_owner.id
        data['list_owner'] = self.possessive_ending(list_owner.get_username())
        return data

        