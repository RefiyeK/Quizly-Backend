from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """Erlaubt Zugriff nur dem Besitzer des Quiz."""

    def has_object_permission(self, request, view, obj):
        """Prüft, ob das Objekt dem aktuellen Benutzer gehört."""
        return obj.owner == request.user