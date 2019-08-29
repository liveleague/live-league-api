from rest_framework import permissions


class IsSuperuserAndStaff(permissions.BasePermission):
    """Checks if the current user is a verified promoter."""

    def has_permission(self, request, view):
        return bool(
            request.user.is_superuser and request.user.is_staff
        )
