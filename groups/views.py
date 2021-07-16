from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.urls.base import reverse_lazy
from accounts.models import CustomUser
from .models import CustomGroup
from .forms import GroupMemberCreateForm
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
)
from django.views.generic import (
    CreateView,
    ListView,
)

class GroupCreateView(
    LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = CustomGroup
    context_object_name = 'group'
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
    LoginRequiredMixin, CreateView):
    form_class = GroupMemberCreateForm
    template_name = 'group/create_member.html'
    
    def get_success_url(self, pk):
        return reverse('group_members', kwargs={'pk': pk})

    def form_valid(self, form):
        form.instance.is_leader = False
        self.object = form.save()
        if self.object.responsible_by == None:
            self.object.responsible_by = self.object
        self.object.save()
        group = CustomGroup.objects.get(pk=self.kwargs['pk'])
        group.user_set.add(self.object)
        return HttpResponseRedirect(self.get_success_url(self.kwargs['pk']))

    def get_form_kwargs(self):
        kwargs = super(GroupMemberCreateView, self).get_form_kwargs()
        group = CustomGroup.objects.get(id=self.kwargs['pk'])

        kwargs['group'] = group
        return kwargs

    def test_func(self):
        current_group = CustomGroup.objects.filter(pk=self.kwargs['pk'])
        return current_group.leader == self.request.user

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

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        group = CustomGroup.objects.get(id=self.kwargs['pk'])
        data['group_id'] = group.id
        data['group_name'] = group.name
        data['form'] = GroupMemberCreateForm(group=group)
        data['leader'] = group.leader == self.request.user
        return data

    def test_func(self):
        group = CustomGroup.objects.get(id=self.kwargs['pk'])
        return self.request.user in group.user_set.all() 
