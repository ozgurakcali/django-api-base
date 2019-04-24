

class Messages:
    """
    Message texts are kept in the Message model. Each message has its own key.
    The keys are formed according to the following notation: "AppId_ModelId_MessageId"
    """

    TOKEN__AUTHENTICATION_FAILED = '2_0_0'
    TOKEN__LOGOUT_SUCCESS = '2_0_1'
    TOKEN__INVALID = '2_0_2'
    TOKEN__PERMISSION_DENIED = '2_0_3'

    def __init__(self):
        pass
