from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from app.domain.entities.price import Price
from app.domain.repositories.price_repo import IPriceRepository


class PriceService:
    def __init__(self, price_repo: IPriceRepository):
        self._repo = price_repo

    async def record_price(self, coin_id: UUID, value: float) -> None:
        """Record a new price for a given coin."""

        price = Price(
            id=uuid4(),
            coin_id=coin_id,
            price=value,
        )
        await self._repo.add(price)

    async def list_prices_by_coin(
        self,
        coin_id: UUID,
        *,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 100,
        offset: int = 0,
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

        return await self._repo.get_latest(coin_id)
