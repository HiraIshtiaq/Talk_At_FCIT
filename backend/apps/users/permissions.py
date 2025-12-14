"""
Custom permissions for user-related operations.
"""
from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Allow owners to edit their own profile."""
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj == request.user


class IsModeratorOrAdmin(permissions.BasePermission):
    """Allow only moderators and admins."""
    
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.role in ['moderator', 'admin']
        )


class IsAdmin(permissions.BasePermission):
    """Allow only admins."""
    
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.role == 'admin'
        )
