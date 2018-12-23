

class InvalidRequestException(Exception):
    """
    Wrapper Exception
    """

    def __init__(self, message):
        super(InvalidRequestException, self).__init__(message)


