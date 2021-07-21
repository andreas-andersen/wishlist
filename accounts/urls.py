# accounts/urls.py
from django.urls import path
from .views import (
    CustomUserLoginView,
    CustomUserSignupView,
    CustomUserDetailView,
    MyWishListsView,
    RecWishListsView, 
    complete_user_activation,
)
from wishlist.views import (
    WishListView,
)

urlpatterns = [
    path('signup_user/', CustomUserSignupView.as_view(), name='signup_user'),
    path('login_user/', CustomUserLoginView.as_view(), name='login_user'),
    path('<int:user_id>/activate/', complete_user_activation, name='activate'),
    path('my_lists/', MyWishListsView.as_view(), name='my_lists'),
    path('received_lists/', RecWishListsView.as_view(), name='received_lists'),
    path('<int:pk>/wish_lists', WishListView.as_view(), name='wish_list'),
    path('<int:pk>/', CustomUserDetailView.as_view(), name='user_details')
]