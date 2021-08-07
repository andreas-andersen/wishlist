import datetime
import numpy as np
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
from accounts.models import CustomUser, Notification
from accounts.tokens import invitation_token
from wishlist.models import Wish
from .assignments import userwise_assignment, random_assignment
from .models import (
    CustomGroup, 
    Assignment,
    Assignments,
)
from .forms import (
    GroupCreateForm,
    GroupMemberCreateForm,
    GroupMemberInviteForm,
    AssignmentForm,
    SelectAssignmentForm,
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
        return CustomGroup.objects.filter(user=self.request.user).order_by('-created')

class GroupMembersListView(
        LoginRequiredMixin, 
        UserPassesTestMixin, 
        ListView,
):
    model = CustomUser
    context_object_name = 'group_members'
    template_name = 'group/members.html'

    def get_queryset(self):
        group = CustomGroup.objects.get(id=self.kwargs['pk'])
        group_leader = group.leader
        return group.user_set.all().exclude(id=group_leader.id).order_by('date_joined')

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

    if ((current_group.leader == request.user or 
            current_user.is_responsible == request.user) and not
                current_group.closed):

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
                        new_notification = Notification(
                            user=existing_user,
                            type='INV',
                            group=current_group,
                            context_user=current_user,
                            content=(
                                f'You have received an invitaion from <b>{current_user.first_name} '
                                f'{current_user.last_name}</b> to join to group <b>{current_group.name}</b>!')
                        )
                        new_notification.save()
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

        if CustomGroup.objects.filter(invited_users=user).exists():
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
def accept_notification_invitation_view(request, group_id, user_id, notification_id):
    current_user = CustomUser.objects.get(id=user_id)
    current_group = CustomGroup.objects.get(id=group_id)
    current_notification = Notification.objects.get(id=notification_id)

    if (current_user == request.user and not current_group.closed and
            current_user in current_group.invited_users.all()):
        current_group.invited_users.remove(current_user)
        current_group.user_set.add(current_user)
        current_group.save()

        current_notification.read = True
        current_notification.save()

        new_notification = Notification(
            user=current_group.leader,
            type='ETC',
            context_user=current_user,
            content=(
                f'<b>{current_user.first_name} {current_user.last_name}</b> has accepted your invitation to join ' 
                f'''<a href="{reverse('group_members', kwargs={'pk': group_id})}">{current_group.name}</a>!''')
        )
        new_notification.save()
        
        return redirect('notifications', user_id)
    
    else:
        return HttpResponseForbidden()

@login_required
def decline_notification_invitation_view(request, group_id, user_id, notification_id):
    current_user = CustomUser.objects.get(id=user_id)
    current_group = CustomGroup.objects.get(id=group_id)
    current_notification = Notification.objects.get(id=notification_id)

    if (current_user == request.user and not current_group.closed and
            current_user in current_group.invited_users.all()):
        current_group.invited_users.remove(current_user)
        current_group.save()

        current_notification.read = True
        current_notification.save()

        new_notification = Notification(
            user=current_group.leader,
            type='ETC',
            context_user=current_user,
            content=(
                f'<b>{current_user.first_name} {current_user.last_name}</b> has declined your invitation to join ' 
                f'''<a href="{reverse('group_members', kwargs={'pk': group_id})}">{current_group.name}</a>''')
        )
        new_notification.save()
        
        return redirect('notifications', user_id)
    
    else:
        return HttpResponseForbidden()


@login_required
def group_member_create_view(request, group_id, user_id):
    current_group = CustomGroup.objects.get(id=group_id)
    current_user = CustomUser.objects.get(id=user_id)

    if current_user.is_self_responsible and not current_group.closed:
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

                if current_user != current_group.leader:
                    new_notification = Notification(
                        user=current_group.leader,
                        type='ETC',
                        context_user=new_user,
                        content=(
                            f'<b>{new_user.first_name} {new_user.last_name}</b> has been added by '
                            f'<b>{current_user.first_name} {current_user.last_name}</b> to the group ' 
                            f'''<a href="{reverse('group_members', kwargs={'pk': group_id})}">{current_group.name}</a>!''')
                    )
                    new_notification.save()

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
    if ((current_group.leader == request.user or 
            current_user.responsible_by == request.user) and not
                current_group.closed):
        current_group.user_set.remove(current_user)
        return redirect('group_members', group_id)
    else:
        return HttpResponseForbidden()
        
@login_required
def uninvite_user_from_group(request, group_id, user_id):
    current_group = CustomGroup.objects.get(id=group_id)
    current_user = CustomUser.objects.get(id=user_id)
    if current_group.leader == request.user and not current_group.closed:
        current_group.invited_users.remove(current_user)
        return redirect('group_members', group_id)        
    else:
        return HttpResponseForbidden()


@login_required
def select_assignment_view(request, group_id):
    current_group = CustomGroup.objects.get(id=group_id)
    if current_group.leader == request.user and not current_group.closed:
        if request.method == 'POST':
            form = SelectAssignmentForm(request.POST)

            if form.is_valid():
                assignment_rule = form.cleaned_data['assignment_rule']
                current_group.assignment_rule = assignment_rule
                current_group.save()

                if assignment_rule == 'M':
                    return redirect('manual_assignment', group_id)
                elif assignment_rule == 'U':
                    return redirect('random_assignment', group_id, 1)
                else:
                    return redirect('random_assignment', group_id, 0)
        
        else:
            form = SelectAssignmentForm()
            has_members = len(current_group.user_set.all()) > 1
            past_deadline = datetime.date.today() > current_group.deadline
            has_wishlists = all(
                [len(Wish.objects.filter(author=user).filter(group=current_group)) > 0 
                    for user in current_group.user_set.all()])

        return render(
            request, 'group/assignment/select.html', 
            {
                'group_id': group_id, 'has_members': has_members,
                'past_deadline': past_deadline, 'has_wishlists': has_wishlists}
        )

@login_required
def manual_assignment_view(request, group_id):
    current_group = CustomGroup.objects.get(id=group_id)
    if current_group.leader == request.user and not current_group.closed:
        if request.method == 'POST':
            form = AssignmentForm(request.POST, group=current_group)

            if form.is_valid():
                cleaned_data = form.cleaned_data['assignments']
                assignments = [(key.strip('assignment_'), values) for key, values in cleaned_data]
                output = [(CustomUser.objects.get(id=key), CustomUser.objects.get(id=value)) 
                    for key, value in assignments]

                request.session['assignments'] = assignments
                return render(
                    request, 'group/assignment/manual_output.html',
                    {'output': output, 'group_id': group_id}
                )
        else:
            form = AssignmentForm(group=current_group)

        return render(
            request, 'group/assignment/manual.html', 
            {'form': form, 'group_id': group_id,}
        )    

    else:
        return HttpResponseForbidden()

@login_required
def random_assignment_view(request, group_id, userwise):
    current_group = CustomGroup.objects.get(id=group_id)
    if current_group.leader == request.user and not current_group.closed:
        if request.method == 'POST':
            form = AssignmentForm(request.POST, group=current_group)

            if form.is_valid():
                cleaned_data = form.cleaned_data['assignments']
                assignments = [(key.strip('assignment_'), values) for key, values in cleaned_data]
                output = [(CustomUser.objects.get(id=key), CustomUser.objects.get(id=value)) 
                    for key, value in assignments]

                request.session['assignments'] = assignments
                return render(
                    request, 'group/assignment/manual_output.html',
                    {'output': output, 'group_id': group_id}
                )
        
        else:
            current_users = current_group.user_set.all()

            users = np.array([user.id for user in current_users])
            responsible = np.array([user.responsible_by.id for user in current_users])
            assignments = np.zeros(len(users), dtype=np.int32)
            assigned = np.zeros(len(users), dtype=bool)
            received_assignments = np.zeros(len(users), dtype=bool)

            assignment_array = np.vstack((users, responsible, assignments, assigned, received_assignments))
            if userwise == True:
                assigned_array = userwise_assignment(assignment_array)[2]
            else:
                assigned_array = random_assignment(assignment_array)[2]
            assigned_users = [CustomUser.objects.get(id=user) for user in assigned_array]

            form = AssignmentForm(group=current_group, assignments=assigned_users)
            return render(
                request, 'group/assignment/random.html', 
                {'form': form, 'group_id': group_id, 'userwise': userwise}
            )

    else:
        return HttpResponseForbidden()


@login_required
def assign(request, group_id):
    current_group = CustomGroup.objects.get(id=group_id)

    if current_group.leader == request.user and not current_group.closed:
        new_assignments = Assignments(group = current_group)
        new_assignments.save()
        assignments = request.session["assignments"]
        user_assignments = [(CustomUser.objects.get(id=key), CustomUser.objects.get(id=value)) 
            for key, value in assignments]

        for member, assignment in user_assignments:
            new_assignment = Assignment(
                member = member,
                assignment = assignment
            )
            new_assignment.save()
            new_assignments.assignments.add(new_assignment)

            responsible_user = assignment.responsible_by,
            new_notification = Notification(
                user=responsible_user,
                type='ETC',
                context_user=member,
                content=(
                    f'<b>{member.first_name} {member.last_name}</b> has been assigned to you in the group ' 
                    f'''<a href="{reverse('group_members', kwargs={'pk': group_id})}">{current_group.name}</a>!'''
                    f'''<br>Check out the <a href="{reverse('received_lists', kwargs={'user_id': responsible_user.id})}">'''
                    f'Received Lists</a> page for details!')
            )
            new_notification.save()
        
        current_group.closed = True
        current_group.save()

        return redirect('group_members', group_id)

    else:
        return HttpResponseForbidden()