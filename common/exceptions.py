from common.constants import MessageTypes
from rest_framework.exceptions import ErrorDetail, PermissionDenied
from rest_framework.response import Response
from rest_framework.utils.serializer_helpers import ReturnDict
from rest_framework.views import exception_handler
from rest_framework import status, exceptions
from rest_framework.serializers import ValidationError

from common.helper_functions import get_message_object
from authentication.constants import Messages as AuthenticationMessages


class InvalidTokenException(exceptions.AuthenticationFailed):
    """
    Exception to be raised when provided jwt token is invalid
    """
    pass


class LoginFailureException(exceptions.AuthenticationFailed):
    """
    Exception to be raised when an authentication attempt fails
    """
    pass


def process_error_list(exception_detail, messages, parent_key=None):
    """
    Process validations errors in a recursive manner, adding each message to messages list.
    Errors may be returned in multiple levels in case of nested serializer usage
    """

    if type(exception_detail) is list:
        # Custom generated exception, not related to a field. Use directly.
        for exception_data in exception_detail:
            messages.append(exception_data)

    elif type(exception_detail) == ReturnDict:
        # List of errors related to a field, raised from a serializer. Go over the fields
        for key in exception_detail:

            if key == 'non_field_errors':
                # Raised from generic validate method of a serializer
                for error in exception_detail[key]:
                    messages.append(error)

            else:
                exception_data = exception_detail[key]

                if type(exception_data) is list:
                    # If multiple messages returned for same field, use only the first
                    exception_data = exception_data[0]

                if type(exception_data) == ErrorDetail:
                    # DRF generated error, build message object here
                    if parent_key:
                        error_message = (parent_key.capitalize() + ' ' + key.capitalize()) + ': ' + exception_data
                    else:
                        error_message = key.capitalize() + ': ' + exception_data

                    messages.append({
                        'key': None,
                        'type': MessageTypes.ERROR,
                        'body': error_message
                    })

                elif type(exception_data) is dict:
                    if 'key' in exception_data:
                        # Custom generated exception. Use directly
                        messages.append(exception_detail[key][0])
                    else:
                        # Second level validation error
                        process_error_list(exception_data, messages, key)


def base_exception_handler(exc, context):
    """
    Global exception handler.
    """

    if isinstance(exc, ValidationError):
        messages = []

        process_error_list(exc.detail, messages)

        response = Response({}, status.HTTP_400_BAD_REQUEST)
        response.messages = messages

        return response

    elif isinstance(exc, InvalidTokenException):
        response = Response({}, status.HTTP_401_UNAUTHORIZED)
        response.messages = [get_message_object(AuthenticationMessages.TOKEN__INVALID)]

        return response

    elif isinstance(exc, LoginFailureException):
        response = Response({}, status.HTTP_401_UNAUTHORIZED)
        response.messages = [get_message_object(AuthenticationMessages.TOKEN__AUTHENTICATION_FAILED)]

        return response

    elif isinstance(exc, PermissionDenied):
        response = Response({}, status.HTTP_403_FORBIDDEN)
        response.messages = [get_message_object(AuthenticationMessages.TOKEN__PERMISSION_DENIED)]

        return response

    # Call default DRF exception handler if not returned above
    return exception_handler(exc, context)
