from django.contrib.auth.models import AbstractUser
from django.db import models

from profiles.constants import RoleTypes


class User(AbstractUser):
    """
    Custom user model, adding no extra fields to fields defined in Django's AbstractUser
    """
    pass

    def __unicode__(self):
        return self.username


class Role(models.Model):
    """
    Model to keep possible roles
    """

    ROLE_TYPE_CHOICES = (
        (RoleTypes.END_USER, 'End User'),
        (RoleTypes.ADMINISTRATOR, 'Administrator'),
    )

    type = models.SmallIntegerField(unique=True, choices=ROLE_TYPE_CHOICES)

    def __unicode__(self):
        return self.type


class UserRole(models.Model):
    """
    Model to keep user - role relations
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='roles')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='users')

    class Meta:
        unique_together = (('user', 'role'),)

    def __unicode__(self):
        return self.user.email + ' - ' + str(self.role.type)
