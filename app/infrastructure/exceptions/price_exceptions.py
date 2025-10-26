from fastapi import HTTPException, status


class PriceNotAvailableError(HTTPException):
    def __init__(self, coin_ticker: str):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f'Failed to fetch price for {coin_ticker}.',
        )
