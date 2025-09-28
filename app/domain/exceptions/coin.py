class CoinTickerAlreadyExistsError(Exception):
    def __init__(self, ticker: str):
        message = f'Coin with ticker {ticker} already exists.'
        super().__init__(message)


class CoinNameAlreadyExistsError(Exception):
    def __init__(self, name: str):
        message = f'Coin with name {name} already exists.'
        super().__init__(message)


class CoinNotFoundError(Exception):
    def __init__(self):
        message = 'Coin not found.'
        super().__init__(message)
