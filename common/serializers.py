from rest_framework import serializers

from common.models import Message


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ('key', 'type', 'body',)
