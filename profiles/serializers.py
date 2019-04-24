from django.contrib.auth import authenticate
from rest_framework import serializers

from common.helper_functions import get_message_object
from profiles.constants import Messages, RoleTypes
from profiles.models import User, UserRole, Role


class UserRoleSerializer(serializers.ModelSerializer):
    """
    Serializer class for UserRole model, to be used as a nested field on UserSerializer
    """

    role_type = serializers.IntegerField(source='role.type')

    class Meta:
        model = UserRole
        fields = ('role_type',)


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer class for User model
    """

    password = serializers.CharField(write_only=True, required=False)
    password_confirm = serializers.CharField(write_only=True, required=False)

    roles = UserRoleSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = ('id',
                  'first_name',
                  'last_name',
                  'email',
                  'username',
                  'password',
                  'password_confirm',
                  'settings',
                  'roles')

    def validate(self, data):
        if not self.instance:
            password = data.get('password')
            password_confirm = data.get('password_confirm')

            # Check that both password provided
            if not (password and password_confirm):
                raise serializers.ValidationError([get_message_object(Messages.USER__PASSWORD_MISSING)])

            # Check that password match
            if password != password_confirm:
                raise serializers.ValidationError([get_message_object(Messages.USER__PASSWORDS_DO_NOT_MATCH)])

        return data

    def create(self, validated_data):
        # Pop settings data if provided
        try:
            validated_data.pop('settings')
        except KeyError:
            pass

        # Create user
        user = User.objects.create_user(username=validated_data.get('username'),
                                        email=validated_data.get('email'),
                                        password=validated_data.get('password'))

        # Set additional user fields
        user.first_name = validated_data.get('first_name')
        user.last_name = validated_data.get('last_name')
        user.save()

        # Add end user role
        UserRole.objects.create(user=user, role=Role.objects.get(type=RoleTypes.END_USER))

        return user

    def update(self, instance, validated_data):
        # Update UserSettings first
        try:
            settings_data = validated_data.pop('settings')
        except KeyError:
            settings_data = None

        if settings_data:
            instance.settings.expected_daily_calories = \
                settings_data.get('expected_daily_calories', instance.settings.expected_daily_calories)
            instance.settings.save()

        # Now update user fields
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)

        instance.save()

        return instance


class SimpleUserSerializer(serializers.ModelSerializer):
    """
    Serializer class for User model, to be used as field in other serializers
    """

    class Meta:
        model = User
        fields = ('id',
                  'first_name',
                  'last_name',
                  'username')


class PasswordUpdateSerializer(serializers.Serializer):
    """
    Serializer class to update user passwords
    """

    username = serializers.CharField(write_only=True)
    current_password = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    def validate(self, data):
        # Check that provided current password is valid
        user = authenticate(username=data.get('username'),
                            password=data.get('current_password'))
        if not user:
            raise serializers.ValidationError([get_message_object(Messages.USER__INVALID_PASSWORD)])

        # Check that password match
        password = data.get('password')
        password_confirm = data.get('password_confirm')

        if password != password_confirm:
            raise serializers.ValidationError([get_message_object(Messages.USER__PASSWORDS_DO_NOT_MATCH)])

        return data

    def create(self, validated_data):
        # Update user password
        user = authenticate(username=validated_data.get('username'),
                            password=validated_data.get('current_password'))

        user.set_password(validated_data.get('password'))
        user.save()

        return user

    def update(self, instance, validate_data):
        return instance


class UserRoleManagementSerializer(serializers.ModelSerializer):
    """
    Serializer class for UserRole model, to be used for modifications
    """

    class Meta:
        model = UserRole
        fields = '__all__'
