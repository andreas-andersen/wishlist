# accounts/urls.py
from django.urls import path
from .views import (
    SignUpView,
    MyWishListsView,
    RecWishListsView, 
    GroupCreateView,
    MyGroupsListView,
    GroupMembersListView,
)
from wishlist.views import (
    WishListView,
)

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('create_group/', GroupCreateView.as_view(), name='create_group'),

    path('my_lists/', MyWishListsView.as_view(), name='my_lists'),
    path('received_lists/', RecWishListsView.as_view(), name='received_lists'),
    path('wish_lists/<int:pk>/', WishListView.as_view(), name='wish_list'),     
    
    path('my_groups/', MyGroupsListView.as_view(), name='my_groups'), 
    path('my_groups/<int:pk>/group_list', GroupMembersListView.as_view(), name='group_members'),
]