import json

from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from authentication.constants import Messages
from authentication.models import JwtToken
from authentication.serializers import TokenSerializer
from common.helper_functions import get_message_object
from profiles.serializers import UserSerializer


class LoginView(GenericAPIView):
    """
    Validate username and password through TokenSerializer and return the token
    """

    serializer_class = TokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Successful authentication. Save token
        serializer.save()

        # Prepare response serializer
        response_serializer = UserSerializer(serializer.context.get('user'))
        response = Response(response_serializer.data)

        # Add token to header
        response['x-authtoken'] = serializer.instance.token

        return response


class MeView(GenericAPIView):
    """
    Get currently authenticated user
    """

    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class LogoutView(GenericAPIView):
    """
    Invalidates currently logged in user's token
    """

    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
        JwtToken.objects.get(token=token).delete()

        return Response({}, headers={
            'Messages': json.dumps([get_message_object(Messages.TOKEN__LOGOUT_SUCCESS)])
        })
