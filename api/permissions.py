from rest_framework.permissions import BasePermission
from django.utils import timezone


class IsEventOrganizer(BasePermission):
    message = "You must be the owner of this event"

    def has_object_permission(self, request, view, obj):
        if obj.organizer == request.user:
            return True
        else:
            return False


# I may use it later
class IsChangeable(BasePermission):
    message = "Old events cannot be cancelled or modified"

    def has_object_permission(self, request, view, obj):
        if obj.datetime > timezone.now():
            return True
        else:
            return False
