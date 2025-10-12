from abc import ABC, abstractmethod
from typing import Any, Optional


class ICache(ABC):
    """Abstract cache interface (e.g. Redis)."""

    @abstractmethod
    async def get(self, key: str) -> Optional[Any]:
        """Get value by key."""

    @abstractmethod
    async def set(
        self, key: str, value: Any, expire_seconds: Optional[int] = None
    ) -> None:
        """Set value with optional expiration."""

    @abstractmethod
    async def delete(self, key: str) -> None:
        """Delete a cache entry."""

    @abstractmethod
    async def exists(self, key: str) -> bool:
        """Check if a key exists."""
