#wishlist/urls.py
from django.urls import path
from .views import (
    WishDetailView, 
    WishListView, 
    WishCreateView, 
    WishUpdateView,
    WishDeleteView,
)

urlpatterns = [
    path('wish/<int:pk>/', WishDetailView.as_view(), name='wish_detail'),
    path('wish/new/', WishCreateView.as_view(), name='wish_new'),
    path('wish/<int:pk>/update/', 
        WishUpdateView.as_view(), name='wish_update'),
    path('wish/<int:pk>/delete/',
        WishDeleteView.as_view(), name='wish_delete'),
    path('', WishListView.as_view(), name='home'),
]