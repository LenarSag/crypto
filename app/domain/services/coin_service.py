from uuid import UUID, uuid4

from app.domain.entities.coin import Coin
from app.domain.exceptions.coin import (
    CoinNameAlreadyExistsError,
    CoinNotFoundError,
    CoinTickerAlreadyExistsError,
)
from app.domain.repositories.coin_repo import ICoinRepository


class CoinService:
    def __init__(self, repo: ICoinRepository):
        self._repo = repo

    async def create_coin(self, ticker: str, name: str) -> Coin:
        """Create a new coin entity and persist it."""

        coin = await self._repo.get_by_ticker(ticker)
        if coin:
            raise CoinTickerAlreadyExistsError(ticker)
        coin = await self._repo.get_by_name(name)
        if coin:
            raise CoinNameAlreadyExistsError(name)

        coin = Coin(
            id=uuid4(),
            ticker=ticker,
            name=name,
        )
        await self._repo.add(coin)
        return coin

    async def get_coin_by_id(self, coin_id: UUID) -> Coin:
        """Retrieve a coin entity by its ID."""

        coin = await self._repo.get_by_id(coin_id)
        if not coin:
            raise CoinNotFoundError()
        return coin

    async def list_coins(self, offset: int = 0, limit: int = 100) -> list[Coin]:
        """List all coins with pagination."""

        return await self._repo.list_coins(offset=offset, limit=limit)

    async def update_coin(self, coin_id: UUID, ticker: str, name: str) -> Coin:
        """Update an existing coin's details."""

        coin = await self._repo.get_by_id(coin_id)
        if not coin:
            raise CoinNotFoundError()

        existing_ticker = await self._repo.get_by_ticker(ticker)
        if existing_ticker and existing_ticker.id != coin_id:
            raise CoinTickerAlreadyExistsError(ticker)

        existing_name = await self._repo.get_by_name(name)
        if existing_name and existing_name.id != coin_id:
            raise CoinNameAlreadyExistsError(name)

        coin.ticker = ticker
        coin.name = name
        await self._repo.update(coin)
        return coin

    async def delete_coin(self, coin_id: UUID) -> None:
        """Delete a coin by its ID."""

        coin = await self._repo.get_by_id(coin_id)
        if not coin:
            raise CoinNotFoundError()
        await self._repo.delete(coin_id)
