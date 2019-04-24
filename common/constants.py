

class Messages:
    """
    Message texts are kept in the Message model. Each message has its own key.
    The keys are formed according to the following notation: "AppId_ModelId_MessageId"
    """

    UNHANDLED_ERROR = '0_0_0'
    REQUEST_PARAMETER_MISSING = '0_0_1'
    HEADER_PARAMETER_MISSING = '0_0_2'
    REQUEST_PARAMETER_INVALID = '0_0_3'

    def __init__(self):
        pass


class MessageTypes:
    """
    Values for message types.
    """

    INFO = 'INFO'
    SUCCESS = 'SUCCESS'
    WARNING = 'WARNING'
    ERROR = 'ERROR'

    def __init__(self):
        pass
