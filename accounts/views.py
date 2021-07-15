from accounts.forms import CustomUserCreationForm
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from .models import CustomGroup, CustomUser
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
)
from django.views.generic import (
    ListView, 
    CreateView,
)

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class MyWishListsView(LoginRequiredMixin, ListView):
    model = CustomUser
    context_object_name = 'my_lists'
    template_name = 'wish/my_lists.html'

    def get_queryset(self):
        return CustomUser.objects.filter(responsible_by=self.request.user)

class RecWishListsView(LoginRequiredMixin, ListView):
    model = CustomUser
    context_object_name = 'received_lists'
    template_name = 'wish/received_lists.html'

    def get_queryset(self):
        matched_responsibilities = CustomUser.objects.filter(responsible_by=self.request.user)
        return CustomUser.objects.filter(assigned_to__in=matched_responsibilities)


class GroupCreateView(
    LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = CustomGroup
    template_name = 'registration/group.html'
    fields = ['name']

    def get_success_url(self, pk):
        return reverse('group_members', kwargs={'pk': pk})
    
    def form_valid(self, form):
        self.object = form.save()
        self.object.user_set.add(self.request.user)
        self.object.leader = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url(self.object.pk))

    def test_func(self):
        return self.request.user.is_leader

class GroupMemberCreateView(
    LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = CustomUser
    template_name = 'group/create_member.html'

class MyGroupsListView(LoginRequiredMixin, ListView):
    model = CustomGroup
    context_object_name = 'my_groups'
    template_name = 'group/my_groups.html'

    def get_queryset(self):
        return CustomGroup.objects.filter(user = self.request.user)

class GroupMembersListView(
    LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = CustomUser
    context_object_name = 'group_members'
    template_name = 'group/members.html'

    def get_queryset(self):
        group = CustomGroup.objects.get(id=self.kwargs['pk'])
        return group.user_set.all()

    def test_func(self):
        group = CustomGroup.objects.get(id=self.kwargs['pk'])
        return self.request.user in group.user_set.all() 