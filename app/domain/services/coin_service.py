from uuid import UUID, uuid4

from app.domain.const.constants import KEY_EXPIRATION_SECONDS
from app.domain.entities.coin import Coin, CoinUpdate
from app.domain.exceptions.coin import (
    CoinNameAlreadyExistsError,
    CoinNotFoundError,
    CoinTickerAlreadyExistsError,
)
from app.domain.ports.cache import ICache
from app.domain.repositories.coin_repo import ICoinRepository
from app.infrastructure.cache.cache_serializers import CoinSerializer


class CoinService:
    """Business use-cases for managing coins."""

    def __init__(self, repo: ICoinRepository, cache: ICache):
        self._repo = repo
        self._cache = cache

    async def create_coin(self, ticker: str, name: str, description: str) -> Coin:
        """Create a new coin entity."""

        coin = await self._repo.get_by_ticker(ticker)
        if coin:
            raise CoinTickerAlreadyExistsError(ticker)
        coin = await self._repo.get_by_name(name)
        if coin:
            raise CoinNameAlreadyExistsError(name)

        coin = Coin(id=uuid4(), ticker=ticker, name=name, description=description)
        await self._repo.add(coin)
        return coin

    async def get_coin_by_id(self, coin_id: UUID) -> Coin:
        """Retrieve a coin entity by its ID."""

        cache_key = f'user:{coin_id}'
        cached = await self._cache.get(cache_key)
        if cached:
            return CoinSerializer.deserialize(cached)

        coin = await self._repo.get_by_id(coin_id)
        if not coin:
            raise CoinNotFoundError()

        serialized_coin = CoinSerializer.serialize(coin)
        await self._cache.set(
            cache_key, serialized_coin, expire_seconds=KEY_EXPIRATION_SECONDS
        )

        return coin

    async def list_coins(self, offset: int, limit: int) -> list[Coin]:
        """List all coins with pagination."""

        return await self._repo.list_coins(offset=offset, limit=limit)

    async def update_coin(self, coin_id: UUID, update_data: CoinUpdate) -> Coin:
        """Update an existing coin's details."""

        coin = await self._repo.get_by_id(coin_id)
        if not coin:
            raise CoinNotFoundError()

        if update_data.name and update_data.name != coin.name:
            existing_coin = await self._repo.get_by_name(update_data.name)
            if existing_coin and existing_coin.id != coin_id:
                raise CoinNameAlreadyExistsError(update_data.name)

        values_to_update = update_data.to_update_dict()

        updated_coin = await self._repo.update(coin_id, values_to_update)
        await self._cache.delete(f'coin:{coin_id}')

        return updated_coin

    async def delete_coin(self, coin_id: UUID) -> None:
        """Delete a coin by its ID."""

        coin = await self._repo.get_by_id(coin_id)
        if not coin:
            raise CoinNotFoundError()
        await self._repo.delete(coin_id)
        await self._cache.delete(f'coin:{coin_id}')
