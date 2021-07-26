from django.urls import path
from .views import (
    GroupCreateView,
    delete_group,
    MyGroupsListView,
    GroupMembersListView,
    accept_invitation_view,
    group_member_invite_view,
    group_member_create_view,
    remove_user_from_group,
    uninvite_user_from_group,
)

urlpatterns = [
    path('create_group/', 
        GroupCreateView.as_view(), name='create_group'),
    path('<int:group_id>/delete_group/',
        delete_group, name='delete_group'),
    path('', 
        MyGroupsListView.as_view(), name='my_groups'), 
    path('<int:pk>/group_members', 
        GroupMembersListView.as_view(), name='group_members'),
    path('<int:group_id>/<int:user_id>/create_members', 
        group_member_create_view, name='create_group_member'),
    path('<int:group_id>/<int:user_id>/invite_members', 
        group_member_invite_view, name='invite_group_member'),
    path('<int:group_id>/<int:user_id>/remove', 
        remove_user_from_group, name='remove_group_member'),
    path('<int:group_id>/<int:user_id>/uninvite', 
        uninvite_user_from_group, name='uninvite_user'),
    path('<uidb64>/<token>/accept_invitation',
        accept_invitation_view, name='accept_invitation'),
]
