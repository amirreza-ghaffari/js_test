from rest_framework import permissions


class ManagerPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return request.user.is_manager
