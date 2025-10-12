from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from app.domain.const.constants import DEFAULT_LIMIT, DEFAULT_OFFSET
from app.domain.entities.coin import Coin


class ICoinRepository(ABC):
    @abstractmethod
    async def add(self, coin: Coin) -> None: ...

    @abstractmethod
    async def get_by_id(self, coin_id: UUID) -> Optional[Coin]: ...

    @abstractmethod
    async def get_by_ticker(self, ticker: str) -> Optional[Coin]: ...

    @abstractmethod
    async def get_by_name(self, name: str) -> Optional[Coin]: ...

    @abstractmethod
    async def list_coins(
        self, *, offset: int = DEFAULT_OFFSET, limit: int = DEFAULT_LIMIT
    ) -> List[Coin]: ...

    @abstractmethod
    async def update(self, coin_id: UUID, update_data: dict) -> Coin: ...

    @abstractmethod
    async def delete(self, coin_id: UUID) -> None: ...

    @abstractmethod
    async def get_with_latest_price(self, coin_id: UUID) -> Optional[Coin]: ...

    @abstractmethod
    async def list_with_latest_prices(
        self, *, offset: int = DEFAULT_OFFSET, limit: int = DEFAULT_LIMIT
    ) -> List[Coin]: ...
