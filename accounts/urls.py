# accounts/urls.py
from django.urls import path
from .views import (
    SignUpView,
    MyWishListsView,
    RecWishListsView, 
)
from wishlist.views import (
    WishCreateView, 
    WishListView,
)

urlpatterns = [
    #path('signup/', SignUpView.as_view(), name='signup'),
    path('my_lists/', MyWishListsView.as_view(), name='my_lists'),
    path('received_lists/', RecWishListsView.as_view(), name='received_lists'),
    path('<int:pk>/wish_list/', WishListView.as_view(), name='wish_list'), 
    path('<int:author_id>/new/', WishCreateView.as_view(), name='wish_new'),
]