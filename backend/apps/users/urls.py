"""
URL patterns for users app.
"""
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import UserProfileView, UserDetailView, LogoutView

app_name = 'users'

urlpatterns = [
    # Djoser authentication endpoints (register, activate, password reset)
    path('', include('djoser.urls')),
    
    # JWT token endpoints
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    # User profile endpoints
    path('me/', UserProfileView.as_view(), name='user-profile'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
]
