class BaseError(Exception):

    def __init__(self, message):
        super().__init__(
            "Parser Error %s" % message
        )


class ValidationError(BaseError):

    def __init__(self, message, **kwargs):
        super().__init__(message)
