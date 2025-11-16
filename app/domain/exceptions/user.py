class EmailAlreadyExistsError(Exception):
    def __init__(self, email: str):
        message = f'User with email {email} already exists.'
        super().__init__(message)


class UserNotFoundError(Exception):
    def __init__(self):
        message = 'User not found.'
        super().__init__(message)


class InvalidCredentialsError(Exception):
    def __init__(self):
        message = 'Incorrect email or password.'
        super().__init__(message)


class InactiveUserError(Exception):
    def __init__(self):
        message = 'User is inactive.'
        super().__init__(message)
