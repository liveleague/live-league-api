from rest_framework import permissions


class IsVerifiedPromoter(permissions.BasePermission):
    """Checks if the current user is a verified promoter."""

    def has_object_permission(self, request, view, obj):
        """Check if a promoter is trying to manage a venue or event."""

        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.promoter.is_verified:
            return obj.is_verified == request.user.promoter.is_verified
