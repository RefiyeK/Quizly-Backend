from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """Allows access only to the owner of the quiz."""

    def has_object_permission(self, request, view, obj):
        """Check whether the object belongs to the current user."""
        return obj.owner == request.user
