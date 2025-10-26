class InvalidTokenError(Exception):
    def __init__(self):
        message = 'Could not validate credentials.'
        super().__init__(message)


class TokenExpiredError(Exception):
    def __init__(self):
        message = 'Token has expired.'
        super().__init__(message)
