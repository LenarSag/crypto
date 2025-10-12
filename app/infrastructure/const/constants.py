from datetime import timedelta

SECRET_KEY = 'dummy_secret_key'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 60


# price fetching settings
BASE_CRYPTO_URL = 'https://api.binance.com/api/v3/ticker/price'
MAIN_CURRENCY = 'USDT'

CIRCUIT_BREAKER_FAIL_MAX = 5
CIRCUIT_BREAKER_RESET_TIMEOUT = timedelta(seconds=60)  # in seconds
