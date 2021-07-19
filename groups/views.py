from django.http import HttpResponseRedirect
from django.http.response import HttpResponseForbidden
from django.shortcuts import redirect
from django.urls import reverse
from django.urls.base import reverse_lazy
from accounts.models import CustomUser
from .models import CustomGroup
from .forms import (
    GroupMemberCreateForm,
    GroupMemberInviteForm,
)
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
)
from django.views.generic import (
    CreateView,
    ListView,
)
from django.views.generic.edit import (
    ModelFormMixin,
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

class GroupMemberInviteView(
    LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = GroupMemberInviteForm
    template_name = 'group/invite_member.html'

    def get_success_url(self, pk):
        return reverse('group_members', kwargs={'pk': pk})

    def form_valid(self, form):
        self.object = form.save()
        self.object.is_self_responsible = True
        self.object.responsible_by = self.object
        self.object.save()
        group = CustomGroup.objects.get(pk=self.kwargs['pk'])
        group.invited_users.add(self.object)
        return HttpResponseRedirect(self.get_success_url(self.kwargs['pk']))
    
    def test_func(self):
        current_group = CustomGroup.objects.get(pk=self.kwargs['pk'])
        return current_group.leader == self.request.user

    def get_form_kwargs(self):
        kwargs = super(GroupMemberInviteView, self).get_form_kwargs()
        kwargs['group_id'] = self.kwargs['pk']
        return kwargs

class GroupMemberCreateView(
    LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = GroupMemberCreateForm
    template_name = 'group/create_member.html'
    
    def get_success_url(self, pk):
        return reverse('group_members', kwargs={'pk': pk})

    def form_valid(self, form):
        self.object = form.save()
        self.object.is_self_responsible = False
        self.object.responsible_by = self.request.user
        self.object.save()
        group = CustomGroup.objects.get(pk=self.kwargs['pk'])
        group.user_set.add(self.object)
        return HttpResponseRedirect(self.get_success_url(self.kwargs['pk']))

    def test_func(self):
        current_group = CustomGroup.objects.get(pk=self.kwargs['pk'])
        return current_group.leader == self.request.user

@login_required
def remove_user_from_group(request, group_id, user_id):
    current_group = CustomGroup.objects.get(id=group_id)
    current_user = CustomUser.objects.get(id=user_id)
    if current_group.leader != request.user:
        return HttpResponseForbidden()
    else:
        current_group.user_set.remove(current_user)
        return redirect('group_members', group_id)

@login_required
def uninvite_user_from_group(request, group_id, user_id):
    current_group = CustomGroup.objects.get(id=group_id)
    current_user = CustomUser.objects.get(id=user_id)
    if current_group.leader != request.user:
        return HttpResponseForbidden()
    else:
        current_group.invited_users.remove(current_user)
        return redirect('group_members', group_id)

class MyGroupsListView(LoginRequiredMixin, ListView,):
    model = CustomGroup
    context_object_name = 'my_groups'
    template_name = 'group/my_groups.html'

    def get_queryset(self):
        return CustomGroup.objects.filter(user = self.request.user)

class GroupMembersListView(
    LoginRequiredMixin, 
    UserPassesTestMixin, 
    ListView,
    ModelFormMixin,):
    model = CustomUser
    form_class = GroupMemberInviteForm
    context_object_name = 'group_members'
    template_name = 'group/members.html'

    def get(self, request, *args, **kwargs):
        self.object = None
        self.form = self.get_form(self.form_class)
        return ListView.get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = None
        self.form = self.get_form(self.form_class)

        if self.form.is_valid():
            self.object = self.form.save()

        return self.get(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(GroupMembersListView, self).get_form_kwargs()
        kwargs['group_id'] = self.kwargs['pk']
        return kwargs

    def get_queryset(self):
        group = CustomGroup.objects.get(id=self.kwargs['pk'])
        return group.user_set.all()

    def get_context_data(self, **kwargs):
        data = super(GroupMembersListView, self).get_context_data(**kwargs)
        group = CustomGroup.objects.get(id=self.kwargs['pk'])
        data['group_id'] = group.id
        data['group_name'] = group.name
        data['leader'] = group.leader == self.request.user
        data['leader_id'] = self.request.user.id
        data['invited_users'] = group.invited_users.all()
        data['invite_form'] = self.form
        data['create_form'] = GroupMemberCreateForm()
        
        return data

    def test_func(self):
        group = CustomGroup.objects.get(id=self.kwargs['pk'])
        return self.request.user in group.user_set.all() 
