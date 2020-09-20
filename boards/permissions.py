from rest_framework.permissions import BasePermission


class IsBoardOwner(BasePermission):
    message = "You must be the owner of this booking"

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        else:
            return False
