"""
URL patterns for search app.
"""
from django.urls import path
from .views import search_posts
from .user_views import search_users

app_name = 'search'

urlpatterns = [
    path('posts/', search_posts, name='search-posts'),
    path('users/', search_users, name='search-users'),
]
