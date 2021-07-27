from django.contrib import messages
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect, HttpResponse
from django.http.response import HttpResponseForbidden
from django.shortcuts import redirect, render
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import login
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from accounts.models import CustomUser
from wishlist.models import Wish
from accounts.tokens import invitation_token
from .models import (
    CustomGroup, 
    Assignment,
    Assignments,
)
from .forms import (
    GroupCreateForm,
    GroupMemberCreateForm,
    GroupMemberInviteForm,
    ManualAssignmentForm,
)
from django.contrib.auth.decorators import login_required
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
    form_class = GroupCreateForm
    context_object_name = 'group'
    template_name = 'group/create.html'

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

@login_required
def delete_group(request, group_id):
    current_group = CustomGroup.objects.get(id=group_id)
    group_leader = current_group.leader
    if request.user != group_leader:
        return HttpResponseForbidden()
    else:
        current_group.delete()
        return redirect('my_groups')

class MyGroupsListView(LoginRequiredMixin, ListView,):
    model = CustomGroup
    context_object_name = 'my_groups'
    template_name = 'group/my_groups.html'

    def get_queryset(self):
        return CustomGroup.objects.filter(user = self.request.user)

class GroupMembersListView(
    LoginRequiredMixin, 
    UserPassesTestMixin, 
    ListView,):
    model = CustomUser
    context_object_name = 'group_members'
    template_name = 'group/members.html'

    def get_queryset(self):
        group = CustomGroup.objects.get(id=self.kwargs['pk'])
        return group.user_set.all()

    def get_context_data(self, **kwargs):
        data = super(GroupMembersListView, self).get_context_data(**kwargs)
        group = CustomGroup.objects.get(id=self.kwargs['pk'])
        data['leader'] = group.leader == self.request.user
        data['invitation'] = len(group.invited_users.all())
        data['current_group'] = group
        data['current_user'] = self.request.user
        data['invited_users'] = group.invited_users.all()
        data['invite_form'] = GroupMemberInviteForm()
        data['create_form'] = GroupMemberCreateForm()
        return data

    def test_func(self):
        group = CustomGroup.objects.get(id=self.kwargs['pk'])
        return self.request.user in group.user_set.all() 


@login_required
def group_member_invite_view(request, group_id, user_id):
    current_group = CustomGroup.objects.get(id=group_id)
    current_user = CustomUser.objects.get(id=user_id)

    if (current_group.leader == request.user or 
            current_user.is_responsible == request.user):

        if request.method == 'POST':
            form = GroupMemberInviteForm(request.POST)
            
            if form.is_valid():
                email = form.cleaned_data['email']

                if CustomUser.objects.filter(email=email).exists():
                    existing_user = CustomUser.objects.get(email=email)
                    if existing_user in current_group.user_set.all():
                        messages.error(
                            request, f'User with {email} is already a group-member', 
                            extra_tags='invite')
                        return redirect('group_members', group_id)

                    elif existing_user in current_group.invited_users.all():
                        messages.error(
                            request, f'User with {email} has already been invited',
                            extra_tags='invite')
                        return redirect('group_members', group_id)

                    else:
                        current_group.invited_users.add(existing_user)
                        messages.success(
                            request, f'User with {email} has been invited!',
                            extra_tags='invite')
                        return redirect('group_members', group_id)

                else:
                    new_user = CustomUser(email=email, responsible_by=None)
                    new_user.is_active = False
                    new_user.save()
                    new_user.responsible_by = new_user
                    new_user.save()
                    current_group.invited_users.add(new_user)

                    current_site = get_current_site(request)
                    mail_subject = 'You have received an invitation from Wishlist.app!'
                    message = render_to_string('registration/invitation_email.html', {
                        'user': new_user,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
                        'token': invitation_token.make_token(new_user),
                    })
                    invite_email = EmailMessage(mail_subject, message, to=[email])
                    invite_email.send()
                    messages.success(
                        request, f'User with {email} has been invited!',
                        extra_tags='invite')
                    
                    return redirect('group_members', group_id)
            
            else:
                messages.error(
                    request, 'Please provide a valid email',
                    extra_tags='invite')
                return redirect('group_members', group_id) 

        else: 
            form = GroupMemberInviteForm()
    else:
        return HttpResponseForbidden()

def accept_invitation_view(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and invitation_token.check_token(user, token):
        invited_group = CustomGroup.objects.filter(invited_users=user)[0]
        user.is_active = True
        invited_group.invited_users.remove(user)
        invited_group.user_set.add(user)
        user.save()
        login(request, user)
        return redirect('activate', user.id)
    else:
        return HttpResponse('Activation link is invalid!')

@login_required
def group_member_create_view(request, group_id, user_id):
    current_group = CustomGroup.objects.get(id=group_id)
    current_user = CustomUser.objects.get(id=user_id)

    if current_user.is_self_responsible:
        if request.method == 'POST':
            form = GroupMemberCreateForm(request.POST)

            if form.is_valid():
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                email = str(CustomUser.objects.latest('id').pk + 1) + '@not-an-address.com'
                new_user = CustomUser(
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    responsible_by=current_user,
                    is_self_responsible=False,
                )
                new_user.save()
                current_group.user_set.add(new_user)

                messages.success(request, f'User successfully added!', extra_tags='create')
                return redirect('group_members', group_id)
            
            else:
                messages.error(request, 'Please provide a valid name', extra_tags='create')
                return redirect('group_members', group_id)
            
        else: 
            form = GroupMemberInviteForm()
    else:
        return HttpResponseForbidden()

@login_required
def remove_user_from_group(request, group_id, user_id):
    current_group = CustomGroup.objects.get(id=group_id)
    current_user = CustomUser.objects.get(id=user_id)
    if (current_group.leader == request.user or 
            current_user.is_responsible == request.user):
        current_group.user_set.remove(current_user)
        return redirect('group_members', group_id)
    else:
        return HttpResponseForbidden()
        
@login_required
def uninvite_user_from_group(request, group_id, user_id):
    current_group = CustomGroup.objects.get(id=group_id)
    current_user = CustomUser.objects.get(id=user_id)
    if current_group.leader == request.user:
        current_group.invited_users.remove(current_user)
        return redirect('group_members', group_id)        
    else:
        return HttpResponseForbidden()


@login_required
def manual_assignment_view(request, group_id):
    current_group = CustomGroup.objects.get(id=group_id)
    if current_group.leader == request.user:
        if request.method == 'POST':
            form = ManualAssignmentForm(request.POST, group=current_group)

            if form.is_valid():
                cleaned_data = form.cleaned_data["assignments"]
                assignments = [(key.strip('assignment_'), values) for key, values in cleaned_data]
                output = [(CustomUser.objects.get(id=key), CustomUser.objects.get(id=value)) 
                    for key, value in assignments]

                request.session['assignments'] = assignments
                return render(
                    request, 'group/assignment/manual_output.html',
                    {'output': output, 'group_id': group_id}
                )
        else:
            form = ManualAssignmentForm(group=current_group)

        return render(
            request, 'group/assignment/manual.html', 
            {'form': form, 'group_id': group_id,}
        )    

    else:
        return HttpResponseForbidden()

@login_required
def assign(request, group_id):
    current_group = CustomGroup.objects.get(id=group_id)
    new_assignments = Assignments(group = current_group)
    new_assignments.save()
    assignments = request.session["assignments"]
    user_assignments = [(CustomUser.objects.get(id=key), CustomUser.objects.get(id=value)) 
        for key, value in assignments]

    if current_group.leader == request.user:
        for member, assignment in user_assignments:
            new_assignment = Assignment(
                member = member,
                assignment = assignment
            )
            new_assignment.save()
            new_assignments.assignments.add(new_assignment)

        return redirect('group_members', group_id)

    else:
        return HttpResponseForbidden()