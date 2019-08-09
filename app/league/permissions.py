from rest_framework import permissions


class IsVerifiedPromoter(permissions.BasePermission):
    """Checks if the current user is a verified promoter."""

    def has_permission(self, request, view):
        return bool(
            request.user.is_promoter and request.user.promoter.is_verified
        )


class IsPromoterOrReadOnly(permissions.BasePermission):
    """Only allows the correct promoter to edit object."""

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named 'promoter'.
        try:
            return obj.promoter == request.user.promoter
        except:
            return obj.event.promoter == request.user.promoter


class IsOwner(permissions.BasePermission):
    """
    Only allows the ticket owner to vote.
    This only applies if the ticket is unclaimed (has no owner).
    """

    def has_object_permission(self, request, view, obj):
        if obj.owner is not None:
            return obj.owner == request.user
        else:
            return True
