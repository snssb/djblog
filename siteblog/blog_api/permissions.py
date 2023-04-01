from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS and request.method != 'PATCH':
            return True

        if request.user.is_staff:
            return True

        return obj.author_l == request.user
