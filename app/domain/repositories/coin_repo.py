from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

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
    async def list_coins(self, *, offset: int = 0, limit: int = 100) -> List[Coin]: ...

    @abstractmethod
    async def update(self, coin: Coin) -> None: ...

    @abstractmethod
    async def delete(self, coin_id: UUID) -> None: ...
