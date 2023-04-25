from rest_framework import permissions

from foodapp.models import Restaurant


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Check if user is owner of a menu"""
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner.owner == request.user


class IsRestaurantOwner(permissions.BasePermission):
    """Check if user is an owner of a restaurant"""
    def has_permission(self, request, view):
        return Restaurant.objects.filter(owner=request.user)
