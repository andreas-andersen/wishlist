#wishlist/urls.py
from django.urls import path
from .views import (
    WishDetailView,
    WishListView,
    WishCreateView, 
    WishDetailedCreateView,
    WishUpdateView,
    delete_wish,
)

urlpatterns = [
    path('wish/<int:pk>/', 
        WishDetailView.as_view(), name='wish_detail'),
    path('<int:group_id>/<int:pk>/wish_lists', 
        WishListView.as_view(), name='wish_list'),
    path('wish/<int:group_id>/<int:author_id>/<int:pk>/update/', 
        WishUpdateView.as_view(), name='update_wish'),
    path('wish/<int:group_id>/<int:author_id>/new/', 
        WishCreateView.as_view(), name='create_wish'),
    path('wish/<int:group_id>/<int:pk>/detailed_new/', 
        WishDetailedCreateView.as_view(), name='detailed_create_wish'),
    path('wish/<int:group_id>/<int:wish_id>/delete/',
        delete_wish, name='delete_wish'),
]