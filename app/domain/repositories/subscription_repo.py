from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from app.domain.entities.subscription import Subscription


class ISubscriptionRepository(ABC):
    @abstractmethod
    async def add(self, subscription: Subscription) -> None: ...

    @abstractmethod
    async def get_by_id(self, subscription_id: UUID) -> Optional[Subscription]: ...

    @abstractmethod
    async def list_by_user(
        self, user_id: UUID, *, active_only: bool = True
    ) -> List[Subscription]: ...

    @abstractmethod
    async def list_by_coin(
        self, coin_id: UUID, *, active_only: bool = True
    ) -> List[Subscription]: ...

    @abstractmethod
    async def update(
        self,
        subscription_id: UUID,
        update_data: dict,
    ) -> Subscription: ...

    @abstractmethod
    async def soft_delete(self, subscription_id: UUID) -> None: ...

    @abstractmethod
    async def delete_permanently(self, subscription_id: UUID) -> None: ...
