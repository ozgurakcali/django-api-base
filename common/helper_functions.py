import datetime

from common.constants import Messages
from common.models import Message
from common.serializers import MessageSerializer


def get_message_object(message_key):
    """
    :param message_key: Key for the message
    :return: Message serializer data for the key. If no entry found for message_key, returns a generic error message
    """
    try:
        return MessageSerializer(Message.objects.get(key=message_key)).data
    except Message.DoesNotExist:
        # If no message data provided for message_key, return a default message
        message_data = MessageSerializer(Message.objects.get(key=Messages.UNHANDLED_ERROR)).data

        # Replace 'key' field with provided message_key
        message_data['key'] = message_key

        return message_data


def convert_datetime_to_timestamp(datetime_object):
    """
    :param datetime_object: A python datetime object
    :return: Provided datetime converted to seconds since epoch
    """
    return (datetime_object - datetime.datetime(1970, 1, 1)).total_seconds()
