# domain/ports/message_broker.py

from abc import ABC, abstractmethod
from typing import Any


class IMessageBroker(ABC):
    """Abstract message broker for publishing domain events."""

    @abstractmethod
    async def publish(self, topic: str, message: dict[str, Any]) -> None: ...

    @abstractmethod
    async def subscribe(self, topic: str, handler: Any) -> None: ...
