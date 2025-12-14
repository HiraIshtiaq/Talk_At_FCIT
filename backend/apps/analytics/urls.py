"""
URL patterns for analytics app.
"""
from django.urls import path
from .views import platform_analytics, user_list_admin, suspend_user

app_name = 'analytics'

urlpatterns = [
    path('', platform_analytics, name='platform-analytics'),
    path('users/', user_list_admin, name='user-list-admin'),
    path('users/<int:user_id>/suspend/', suspend_user, name='suspend-user'),
]
