from django.urls import path
from .views import (
    GroupCreateView,
    MyGroupsListView,
    GroupMembersListView,
    GroupMemberCreateView,
    GroupMemberInviteView,
    remove_user_from_group,
    uninvite_user_from_group,
)

urlpatterns = [
    path(
        'create_group/', 
        GroupCreateView.as_view(), 
        name='create_group'
    ),
    path(
        '', 
        MyGroupsListView.as_view(), 
        name='my_groups'
    ), 
    path(
        '<int:pk>/group_members', 
        GroupMembersListView.as_view(), 
        name='group_members'),
    path(
        '<int:pk>/create_members', 
        GroupMemberCreateView.as_view(), 
        name='create_group_member'),
    path(
        '<int:pk>/invite_members', 
        GroupMemberInviteView.as_view(), 
        name='invite_group_member'
    ),
    path(
        '<int:group_id>/<int:user_id>/remove', 
        remove_user_from_group, 
        name='remove_group_member'
    ),
    path(
        '<int:group_id>/<int:user_id>/uninvite', 
        uninvite_user_from_group, 
        name='uninvite_user'
    ),
]
