from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Object-level permission to only allow owners (created_by) to edit/delete patient objects.
    """

    def has_object_permission(self, request, view, obj):
        # Assumes obj has attribute `created_by`
        return getattr(obj, "created_by", None) == request.user
