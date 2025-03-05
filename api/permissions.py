from rest_framework import permissions
from rest_framework.permissions import BasePermission

class OnlyAdminsCanDeletePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == "DELETE":
            return request.user.is_staff
        else:
            return True


class IsCartOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.cart.user == request.user

