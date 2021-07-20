# accounts/urls.py
from django.urls import path
from .views import (
    SignUpView,
    MyWishListsView,
    RecWishListsView, 
    complete_user_activation,
)
from wishlist.views import (
    WishListView,
)

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('<int:user_id>/activate/', complete_user_activation, name='activate'),
    path('my_lists/', MyWishListsView.as_view(), name='my_lists'),
    path('received_lists/', RecWishListsView.as_view(), name='received_lists'),
    path('<int:pk>/wish_lists', WishListView.as_view(), name='wish_list'),
]