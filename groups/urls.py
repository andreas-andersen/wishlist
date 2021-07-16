from django.urls import path
from .views import (
    GroupCreateView,
    MyGroupsListView,
    GroupMembersListView,
    GroupMemberCreateView,
)

urlpatterns = [
    path('create_group/', GroupCreateView.as_view(), name='create_group'),
    path('', MyGroupsListView.as_view(), name='my_groups'), 
    path('<int:pk>/group_members', GroupMembersListView.as_view(), name='group_members'),
    path('<int:pk>/create_members', GroupMemberCreateView.as_view(), name='create_group_member'),
]
    