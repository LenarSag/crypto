from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from app.domain.const.constants import KEY_EXPIRATION_SECONDS
from app.domain.entities.price import Price
from app.domain.exceptions.price import PriceNotAvailableError
from app.domain.ports.cache import ICache
from app.domain.ports.price_provider import IExternalPriceProvider
from app.domain.repositories.price_repo import IPriceRepository
from app.infrastructure.cache.cache_serializers import PriceSerializer


class PriceService:
    """Business use-cases for managing prices."""

    def __init__(
        self,
        price_repo: IPriceRepository,
        price_provider: IExternalPriceProvider,
        cache: ICache,
    ):
        self._repo = price_repo
        self._price_provider = price_provider
        self._cache = cache

    async def record_price(self, coin_id: UUID, value: float) -> None:
        """Record a new price for a given coin."""

        price = Price(
            id=uuid4(),
            coin_id=coin_id,
            price=value,
        )
        await self._repo.add(price)

    async def fetch_and_record_price(self, coin_ticker: str, coin_id: UUID) -> None:
        """Fetch the current price from an external provider and record it."""

        price_value = await self._price_provider.fetch_current_price(coin_ticker)
        if price_value is not None:
            return None

        await self.record_price(coin_id, price_value)

        cache_key = f'price:{coin_id}'
        serialized_price = PriceSerializer.serialize(price_value)
        await self._cache.set(
            cache_key, serialized_price, expire_seconds=KEY_EXPIRATION_SECONDS
        )

    async def list_prices_by_coin(
        self,
        coin_id: UUID,
        *,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int,
        offset: int,
    ) -> list[Price]:
        """List historical prices for a given coin within an optional time range."""

        return await self._repo.list_by_coin(
            coin_id,
            start_date=start_date,
            end_date=end_date,
            limit=limit,
            offset=offset,
        )

    async def get_latest_price(self, coin_id: UUID) -> Optional[Price]:
        """Retrieve the latest price for a given coin. Returns None if no price is found."""

        cache_key = f'price:{coin_id}'
        cached = await self._cache.get(cache_key)
        if cached:
            return PriceSerializer.deserialize(cached)

        price = await self._repo.get_latest(coin_id)
        if not price:
            raise PriceNotAvailableError()

        serialized_price = PriceSerializer.serialize(price)
        await self._cache.set(
            cache_key, serialized_price, expire_seconds=KEY_EXPIRATION_SECONDS
        )

        return price
