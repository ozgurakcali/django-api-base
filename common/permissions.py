from rest_framework import permissions
from profiles.constants import RoleTypes
from profiles.helper_functions import user_has_role


class EndUserPermissions(permissions.BasePermission):
    """
    Allowing only users with Role END_USER
    """

    def has_permission(self, request, view):
        return user_has_role(request.user, RoleTypes.END_USER)

    def has_object_permission(self, request, view, obj):
        return user_has_role(request.user, RoleTypes.END_USER)


class AdministratorPermissions(permissions.BasePermission):
    """
    Allowing only users with Role ADMINISTRATOR
    """

    def has_permission(self, request, view):
        return user_has_role(request.user, RoleTypes.ADMINISTRATOR)

    def has_object_permission(self, request, view, obj):
        return user_has_role(request.user, RoleTypes.ADMINISTRATOR)


class SuperUserPermissions(permissions.BasePermission):
    """
    Allowing only super users
    """

    def has_permission(self, request, view):
        return request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser
