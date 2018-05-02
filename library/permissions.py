from rest_framework import permissions


class IsDIACOM(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_DIACOM


class IsDIACOMOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_DIACOM


class IsOwnerOrDIACOM(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_DIACOM or request.user == obj.id_user
