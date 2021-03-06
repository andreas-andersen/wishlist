# accounts/urls.py
from django.urls import path
from .views import (
    CustomUserLoginView,
    CustomUserPasswordChangeView,
    CustomUserSignupView,
    CustomUserDetailsView,
    NotificationsHistoryView,
    mark_as_read_view,
    mark_all_as_read_view,
    my_wish_lists_view,
    received_lists_view,
    complete_user_activation,
    notifications_center_view,
)

urlpatterns = [
    path('signup_user/', CustomUserSignupView.as_view(), name='signup_user'),
    path('login_user/', CustomUserLoginView.as_view(), name='login_user'),
    path('<int:user_id>/activate/', complete_user_activation, name='activate'),
    path('<int:user_id>/change_password/', CustomUserPasswordChangeView.as_view(), name='change_password'),
    path('<int:pk>/details/', CustomUserDetailsView.as_view(), name='user_details'),
    path('<int:user_id>/notifications/', notifications_center_view, name='notifications'),
    path('<int:user_id>/<notification_id>/mark_as_read/', mark_as_read_view, name='mark_as_read'),
    path('<int:user_id>/mark_all_as_read/', mark_all_as_read_view, name='mark_all_as_read'),
    path('<int:user_id>/notifications_history/', NotificationsHistoryView.as_view(), name='notifications_history'),
    path('<int:user_id>/my_lists', my_wish_lists_view, name='my_lists'),
    path('<int:user_id>/received_lists/', received_lists_view, name='my_received_lists'),
]