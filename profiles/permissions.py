from rest_framework import permissions

from profiles.constants import RoleTypes
from profiles.helper_functions import user_has_role


class UserViewPermissions(permissions.BasePermission):
    """
    Permission class specific to User view
    """

    def has_permission(self, request, view):
        if view.action == 'create':
            # Enable public registration
            return True

        if view.action == 'list':
            # Only administrators can list users
            return request.user.is_authenticated and \
                   (user_has_role(request.user, RoleTypes.ADMINISTRATOR))

        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Administrators or the user itself can has object level permissions on a User instance
        return user_has_role(request.user, RoleTypes.ADMINISTRATOR) or \
               request.user == obj
