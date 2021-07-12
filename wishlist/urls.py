#wishlist/urls.py
from django.urls import path
from .views import (
    HomePageView,
    WishDetailView, 
    WishUpdateView,
    WishDeleteView,
)

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('wish/<int:pk>/', 
        WishDetailView.as_view(), name='wish_detail'),
    path('wish/<int:pk>/update/', 
        WishUpdateView.as_view(), name='wish_update'),
    path('wish/<int:pk>/delete/',
        WishDeleteView.as_view(), name='wish_delete'),
]