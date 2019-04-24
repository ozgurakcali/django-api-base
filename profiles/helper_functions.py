from profiles.models import UserRole


def user_has_role(user, role_type):
    """
    :param user: User object for which the role check will be applied
    :param role_type: Role object for which the role check will be applied
    :return: True if provided user as provided role, False otherwise
    """

    try:
        UserRole.objects.get(user=user,
                             role__type=role_type)
    except UserRole.DoesNotExist:
        return False

    return True
