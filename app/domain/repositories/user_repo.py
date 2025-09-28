from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from app.domain.entities.user import User


class IUserRepository(ABC):
    @abstractmethod
    async def add(self, user: User) -> None: ...

    @abstractmethod
    async def get_by_id(self, uuid: UUID) -> Optional[User]: ...

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]: ...

    @abstractmethod
    async def list_users(self, offset: int = 0, limit: int = 100) -> List[User]: ...

    @abstractmethod
    async def update(self, user: User) -> None: ...

    @abstractmethod
    async def soft_delete(self, user_id: UUID) -> None: ...

    @abstractmethod
    async def delete_permanently(self, user_id: UUID) -> None: ...
