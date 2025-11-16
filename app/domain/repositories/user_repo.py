from abc import ABC, abstractmethod
from typing import Optional, Union
from uuid import UUID

from app.domain.entities.user import User


class IUserRepository(ABC):
    @abstractmethod
    async def add(self, user: User) -> User: ...

    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> Optional[User]: ...

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]: ...

    @abstractmethod
    async def list_users(
        self, offset: int, limit: int
    ) -> dict[str, Union[int, list[User]]]: ...

    @abstractmethod
    async def update(self, user_id: UUID, update_data: dict) -> User: ...

    @abstractmethod
    async def soft_delete(self, user_id: UUID) -> None: ...

    @abstractmethod
    async def delete_permanently(self, user_id: UUID) -> None: ...
