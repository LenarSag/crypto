class PriceNotAvailableError(Exception):
    def __init__(self):
        message = 'Price not found.'
        super().__init__(message)
