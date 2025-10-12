class SubscriptionNotFoundError(Exception):
    def __init__(self):
        message = 'Subscription not found.'
        super().__init__(message)
