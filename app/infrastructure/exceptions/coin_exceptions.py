from fastapi import HTTPException, status


class CoinTickerAlreadyExistsError(HTTPException):
    def __init__(self, ticker: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Coin with ticker {ticker} already exists.',
        )


class CoinNameAlreadyExistsError(HTTPException):
    def __init__(self, name: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Coin with name {name} already exists.',
        )


class CoinNotFoundError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Coin not found.',
        )
