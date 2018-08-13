class BaseError(Exception):
    ERROR_TYPE = 'Parser'

    def __init__(self, message, err_type=None):
        if not err_type:
            err_type = self.ERROR_TYPE
        super().__init__(
            "{} Error: {}".format(err_type, message)
        )


class ValidationError(BaseError):
    ERROR_TYPE = 'Validation'

    def __init__(self, message, err_type=None):
        if not err_type:
            err_type = self.ERROR_TYPE
        super().__init__(message, err_type=err_type)


class ConverError(ValidationError):
    ERROR_TYPE = 'Parser'

    def __init__(self, message):
        super().__init__(message, err_type=self.ERROR_TYPE)