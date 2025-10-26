from fastapi import HTTPException, status


class SubscriptionNotFoundError(HTTPException):
    def __init__(self, subscription_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Subscription with ID {subscription_id} not found.',
        )
