from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from app.domain.entities.price import Price


class IPriceRepository(ABC):
    @abstractmethod
    async def add(self, price: Price) -> None: ...

    @abstractmethod
    async def list_by_coin(
        self,
        coin_id: UUID,
        *,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[Price]: ...

    @abstractmethod
    async def get_latest(self, coin_id: UUID) -> Optional[Price]: ...
