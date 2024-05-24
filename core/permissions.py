from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS
from django.core.exceptions import ObjectDoesNotExist
from core.models import AdminProfile


class BaseAdminPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            print(request.user.profile)
            if request.user and request.user.is_authenticated and request.user.profile:
                return True
            else:
                return False
        except ObjectDoesNotExist:
            return False

    def has_object_permission(self, request, view, obj):
        return True