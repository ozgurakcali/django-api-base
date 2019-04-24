import datetime

import jwt
from django.db import models

from django_api_base.settings import JWT_SECRET
from common.helper_functions import convert_datetime_to_timestamp
from profiles.models import Role


class JwtToken(models.Model):
    token = models.TextField(unique=True)

    @staticmethod
    def generate_jwt_token(user):
        token_validity_limit = 1440  # Minutes

        payload = {
            'iss': 'toptal-calories',
            'exp': convert_datetime_to_timestamp(datetime.datetime.utcnow() +
                                                 datetime.timedelta(minutes=token_validity_limit)),
            'username': user.username,
            'roles': [role.type for role in Role.objects.filter(users__user=user)]
        }

        return jwt.encode(payload, JWT_SECRET).decode('utf-8')

    def __unicode__(self):
        return str(self.id)
