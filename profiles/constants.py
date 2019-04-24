

class Messages:
    """
    Message texts are kept in the Message model. Each message has its own key.
    The keys are formed according to the following notation: "AppId_ModelId_MessageId"
    """

    USER__PASSWORD_MISSING = '1_0_0'
    USER__PASSWORDS_DO_NOT_MATCH = '1_0_1'
    USER__INVALID_PASSWORD = '1_0_2'

    def __init__(self):
        pass


class RoleTypes:
    """
    Values for user role types.
    """

    END_USER = 1
    ADMINISTRATOR = 2

    def __init__(self):
        pass
