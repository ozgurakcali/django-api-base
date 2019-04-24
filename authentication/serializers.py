from django.contrib.auth import authenticate
from rest_framework import serializers

from authentication.models import JwtToken
from common.exceptions import LoginFailureException


class TokenSerializer(serializers.ModelSerializer):

    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)

    class Meta:
        model = JwtToken
        fields = ('username', 'password', 'token',)

    def validate(self, data):
        user = authenticate(username=data.get('username'),
                            password=data.get('password'))
        if not user:
            raise LoginFailureException()

        self.context['user'] = user

        return data

    def create(self, validated_data):
        user = self.context.get('user')

        token = JwtToken.generate_jwt_token(user)
        token_object = JwtToken.objects.create(token=token)

        return token_object
