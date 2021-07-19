#wishlist/urls.py
from django.urls import path
from .views import (
    WishDetailView,
    WishCreateView, 
    WishUpdateView,
    delete_wish,
)

urlpatterns = [
    path('wish/<int:pk>/', 
        WishDetailView.as_view(), name='wish_detail'),
    path('wish/<int:pk>/update/', 
        WishUpdateView.as_view(), name='wish_update'),
    path('wishlist/<int:author_id>/new/', 
        WishCreateView.as_view(), name='wish_new'),
    path('wish/<int:wish_id>/delete/',
        delete_wish, name='delete_wish'),
]