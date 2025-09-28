class SubscriptionNotFoundError(Exception):
    def __init__(self, id: int):
        message = f'Subscription with id {id} not found.'
        super().__init__(message)
