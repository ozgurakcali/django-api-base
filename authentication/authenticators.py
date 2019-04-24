import datetime
import jwt

from authentication.models import JwtToken
from profiles.models import User
from django_api_base.settings import JWT_SECRET
from jwt import DecodeError, ExpiredSignatureError
from rest_framework import authentication


class JwtTokenAuthentication(authentication.BaseAuthentication):
    """
    Custom authentication class to authenticate users with jwt token headers
    """

    def authenticate(self, request):
        from common.exceptions import InvalidTokenException

        auth_header = request.META.get('HTTP_AUTHORIZATION', None)
        if auth_header:
            key, token = auth_header.split(' ')

            if key == 'Bearer':
                # Try to decode jwt token here
                try:
                    payload = jwt.decode(jwt=token, key=JWT_SECRET)
                except DecodeError:
                    # Decode failed, invalid token or not signed with our secret
                    raise InvalidTokenException()
                except ExpiredSignatureError:
                    # Token expired
                    raise InvalidTokenException()
                else:
                    exp = payload.get('exp', None)
                    username = payload.get('username', None)

                    if exp and username:
                        try:
                            expires_on = datetime.datetime.utcfromtimestamp(int(exp))
                        except ValueError:
                            # Invalid exp claim
                            raise InvalidTokenException()
                        else:
                            if expires_on > datetime.datetime.utcnow():
                                try:
                                    JwtToken.objects.get(token=token)
                                except JwtToken.DoesNotExist:
                                    # Invalid token or authenticated with a different device id
                                    raise InvalidTokenException()
                                else:
                                    try:
                                        user = User.objects.get(username=username)
                                    except User.DoesNotExist:
                                        # Invalid username
                                        raise InvalidTokenException()
                                    else:
                                        # Successfully authenticated
                                        return user, None
                            else:
                                # Token expired
                                raise InvalidTokenException()
                    else:
                        # No username or exp in payload
                        raise InvalidTokenException()
            else:
                return None

        return None
