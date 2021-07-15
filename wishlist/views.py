#wishlist/views.py
from django.urls import reverse, reverse_lazy
from .models import Wish
from .forms import WishCreationForm
from accounts.models import CustomUser
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
) 
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

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        
        if self.request.user.is_authenticated:
            data['screen_name'] = get_name_or_username(self.request.user)
        return data
        

class WishDetailView(LoginRequiredMixin, DetailView):
    model = Wish
    context_object_name = 'wish'
    template_name = 'wish/detail.html'

class WishCreateView(
    LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Wish
    context_object_name = 'wish'
    template_name = 'wish/new.html'
    fields = ['title', 'priority', 'details']

    def form_valid(self, form):
        form.instance.author = CustomUser.objects.get(id=self.kwargs['author_id'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('wish_list', kwargs={'pk': self.kwargs['author_id']})

    def test_func(self):
        wish_author = CustomUser.objects.get(id=self.kwargs['author_id'])
        responsible_author = wish_author.responsible_by
        return responsible_author == self.request.user


class WishUpdateView(
    LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Wish
    context_object_name = 'wish'
    template_name = 'wish/update.html'
    fields = ['title', 'priority', 'details']

    def test_func(self):
        wish_author = self.get_object().author
        responsible_author = wish_author.responsible_by
        return responsible_author == self.request.user

class WishDeleteView(LoginRequiredMixin, DeleteView):
    model = Wish
    context_object_name = 'wish'
    template_name = 'wish/delete.html'

    def get_success_url(self):
        return reverse('wish_list', kwargs={'pk': self.get_object().author.pk})

class WishListView(LoginRequiredMixin, ListView):
    model = Wish
    context_object_name = 'wish'
    template_name = 'wish/list.html'
    fields = ['title', 'author', 'priority', 'details']

    def get_queryset(self):
        return Wish.objects.filter(author_id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        list_owner = CustomUser.objects.get(id=self.kwargs['pk'])
        data['list_owner_id'] = list_owner.id
        data['list_owner'] = get_possessive_ending(
            get_name_or_username(list_owner))
        data['form'] = WishCreationForm()
        return data


def get_name_or_username(user):
        if user.first_name:
            return user.first_name
        else:
            return user.username

def get_possessive_ending(word):
        return word + "'" if word[-1] == 's' else word + "'s"