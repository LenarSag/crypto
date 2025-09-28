from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from app.domain.entities.subscription import Subscription


class ISubscriptionRepository(ABC):
    @abstractmethod
    async def add(self, subscription: Subscription) -> None: ...

    @abstractmethod
    async def get_by_id(self, subscription_id: int) -> Optional[Subscription]: ...

    @abstractmethod
    async def list_by_user(
        self, user_id: UUID, *, active_only: bool = True
    ) -> List[Subscription]: ...

    @abstractmethod
    async def list_by_coin(
        self, user_id: UUID, *, active_only: bool = True
    ) -> List[Subscription]: ...

    @abstractmethod
    async def update(
        self,
        subscription: Subscription,
    ) -> None: ...

    @abstractmethod
    async def delete(self, subscription_id: int) -> None: ...
