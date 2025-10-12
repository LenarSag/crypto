class InvalidTokenError(Exception):
    def __init__(self):
        message = 'Invalid credentials email or password.'
        super().__init__(message)
