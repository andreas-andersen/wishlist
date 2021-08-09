from easy_pdf.views import PDFTemplateView
from django.http.response import HttpResponseForbidden
from django.shortcuts import redirect
from django.urls import reverse
from pages.views import get_name_or_email, get_possessive_ending
from .models import Wish
from .forms import (
    WishCreateForm, 
    WishUpdateForm,
    WishDetailedCreateForm,
)
from accounts.models import CustomUser
from groups.models import Assignments, CustomGroup
from django.contrib.auth.decorators import (
    login_required,
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
) 
from django.views.generic import (
    ListView, 
    DetailView,
)
from django.views.generic.edit import (
    CreateView,
    UpdateView, 
)
        
class WishDetailView(LoginRequiredMixin, DetailView):
    model = Wish
    context_object_name = 'wish'
    template_name = 'wish/detail.html'

class WishCreateView(
        LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Wish
    context_object_name = 'wish'
    fields = ['title', 'priority', 'details']

    def form_valid(self, form):
        form.instance.author = CustomUser.objects.get(id=self.kwargs['author_id'])
        form.instance.group = CustomGroup.objects.get(id=self.kwargs['group_id'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'wish_list', 
            kwargs={'group_id': self.kwargs['group_id'], 'pk': self.kwargs['author_id']})

    def test_func(self):
        wish_author = CustomUser.objects.get(id=self.kwargs['author_id'])
        responsible_author = wish_author.responsible_by
        return responsible_author == self.request.user

class WishDetailedCreateView(
        LoginRequiredMixin, 
        UserPassesTestMixin, 
        CreateView
    ):
    model = Wish
    form_class = WishDetailedCreateForm
    context_object_name = 'wish'
    template_name = 'wish/create.html'

    def form_valid(self, form):
        form.instance.author = CustomUser.objects.get(id=self.kwargs['pk'])
        form.instance.group = CustomGroup.objects.get(id=self.kwargs['group_id'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'wish_list', 
            kwargs={'group_id': self.kwargs['group_id'], 'pk': self.kwargs['pk']})

    def test_func(self):
        wish_author = CustomUser.objects.get(id=self.kwargs['pk'])
        responsible_author = wish_author.responsible_by
        return responsible_author.id == self.request.user.id

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['group_id'] = self.kwargs['group_id']
        data['author_id'] = self.kwargs['pk']
        return data

class WishUpdateView(
    LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Wish
    form_class = WishUpdateForm
    context_object_name = 'wish'
    template_name = 'wish/update.html'

    def get_success_url(self):
        return reverse(
            'wish_list', 
            kwargs={'group_id': self.kwargs['group_id'], 'pk': self.kwargs['author_id']})

    def test_func(self):
        wish_author = self.get_object().author
        responsible_author = wish_author.responsible_by
        return responsible_author == self.request.user

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['group_id'] = self.kwargs['group_id']
        data['author_id'] = self.kwargs['author_id']
        data['wish'] = Wish.objects.get(id=self.kwargs['pk'])
        return data

@login_required
def delete_wish(request, group_id, wish_id):
    current_wish = Wish.objects.get(group_id=group_id, id=wish_id)
    owner = current_wish.author
    responsible_user = owner.responsible_by
    if request.user != responsible_user:
        return HttpResponseForbidden()
    else:
        Wish.objects.get(id=wish_id).delete()
        return redirect('wish_list', group_id, owner.id)

class WishListView(LoginRequiredMixin, UserPassesTestMixin,  ListView):
    model = Wish
    context_object_name = 'wish'
    template_name = 'wish/list.html'
    fields = ['title', 'author', 'priority', 'details']

    def get_queryset(self):
        return Wish.objects.filter(author_id=self.kwargs['pk']).filter(group_id=self.kwargs['group_id'])

    def test_func(self):
        wish_author = CustomUser.objects.get(id=self.kwargs['pk'])
        responsible_author = wish_author.responsible_by
        return responsible_author == self.request.user     

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        author = CustomUser.objects.get(id=self.kwargs['pk'])
        data['group_id'] = self.kwargs['group_id']
        data['author_id'] = self.kwargs['pk']
        data['author_name'] = get_possessive_ending(
            get_name_or_email(author))
        data['form'] = WishCreateForm()
        return data

class ReceivedWishListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Wish
    context_object_name = 'wish'
    template_name = 'wish/received_list.html'
    
    def get_queryset(self):
        current_wishes = (Wish.objects.filter(author_id=self.kwargs['pk'])
            .filter(group_id=self.kwargs['group_id']).order_by('-priority'))
        return current_wishes

    def test_func(self):
        current_user = CustomUser.objects.get(id=self.kwargs['pk'])
        current_group = CustomGroup.objects.get(id=self.kwargs['group_id'])
        responsible_users = current_group.user_set.filter(responsible_by=self.request.user)
        current_assignments = Assignments.objects.get(group=current_group)
        current_assignment = current_assignments.assignments.get(assignment=current_user)
        return current_assignment.member in responsible_users

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        current_author = CustomUser.objects.get(id=self.kwargs['pk'])
        current_group = CustomGroup.objects.get(id=self.kwargs['group_id'])
        current_assignments = Assignments.objects.get(group=current_group)
        current_assignment = current_assignments.assignments.get(assignment=current_author).member
        data['current_author'] = current_author
        data['current_group'] = current_group
        data['current_assignment'] = current_assignment
        return data

class ReceivedWishListPrintout(LoginRequiredMixin, UserPassesTestMixin, PDFTemplateView):
    template_name = 'wish/received_printout.html'

    def get_pdf_filename(self):
        current_user = CustomUser.objects.get(id=self.kwargs['author_id'])
        current_user_name = current_user.first_name + ' ' + current_user.last_name
        current_user_name_snake = '_'.join(current_user_name.split())
        return current_user_name_snake + '.pdf'

    def test_func(self):
        current_user = CustomUser.objects.get(id=self.kwargs['author_id'])
        current_group = CustomGroup.objects.get(id=self.kwargs['group_id'])
        responsible_users = current_group.user_set.filter(responsible_by=self.request.user)
        current_assignments = Assignments.objects.get(group=current_group)
        current_assignment = current_assignments.assignments.get(assignment=current_user)
        return current_assignment.member in responsible_users

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        current_author = CustomUser.objects.get(id=self.kwargs['author_id'])
        current_group = CustomGroup.objects.get(id=self.kwargs['group_id'])
        current_assignments = Assignments.objects.get(group=current_group)
        current_assignment = current_assignments.assignments.get(assignment=current_author).member
        current_wishes = Wish.objects.filter(group=current_group).filter(author=current_author)
        data['current_author'] = current_author
        data['current_group'] = current_group
        data['current_assignment'] = current_assignment
        data['current_wishes'] = current_wishes
        return data

class TestView(ListView):
    model = Wish
    context_object_name = 'wish'
    template_name = 'wish/received_printout.html'
    fields = ['title', 'author', 'priority', 'details']

    def get_queryset(self):
        return Wish.objects.filter(author_id=self.kwargs['pk']).filter(group_id=self.kwargs['group_id'])
    