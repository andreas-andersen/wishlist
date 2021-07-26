#wishlist/urls.py
from django.urls import path
from .views import (
    WishDetailView,
    WishCreateView, 
    WishDetailedCreateView,
    WishUpdateView,
    delete_wish,
)

urlpatterns = [
    path('wish/<int:pk>/', 
        WishDetailView.as_view(), name='wish_detail'),
    path('wish/<int:author_id>/<int:pk>/update/', 
        WishUpdateView.as_view(), name='update_wish'),
    path('wish/<int:author_id>/new/', 
        WishCreateView.as_view(), name='wish_new'),
    path('wish/<int:pk>/detailed_new/', 
        WishDetailedCreateView.as_view(), name='wish_detailed_new'),
    path('wish/<int:wish_id>/delete/',
        delete_wish, name='delete_wish'),
]