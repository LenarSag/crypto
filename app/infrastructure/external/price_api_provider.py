import logging
from typing import Optional

from aiobreaker import CircuitBreaker
from httpx import AsyncClient

from app.domain.ports.price_provider import IExternalPriceProvider
from app.infrastructure.const.constants import (
    BASE_CRYPTO_URL,
    CIRCUIT_BREAKER_FAIL_MAX,
    CIRCUIT_BREAKER_RESET_TIMEOUT,
    MAIN_CURRENCY,
)

logger = logging.getLogger(__name__)
breaker = CircuitBreaker(
    fail_max=CIRCUIT_BREAKER_FAIL_MAX, timeout_duration=CIRCUIT_BREAKER_RESET_TIMEOUT
)


class CoinPriceProvider(IExternalPriceProvider):
    """Fetches cryptocurrency prices from an external API."""

    @breaker
    async def fetch_price(self, coin_ticker: str) -> Optional[float]:
        ticker = coin_ticker.upper() + MAIN_CURRENCY
        params = {'symbol': ticker}
        try:
            async with AsyncClient() as client:
                response = await client.get(url=BASE_CRYPTO_URL, params=params)
                response.raise_for_status()
                data = response.json()
                price = data.get('price')
                if price:
                    return round(float(price), 2)
        except Exception as e:
            logger.info(f'Failed to fetch {coin_ticker}: {e}')
            return None
