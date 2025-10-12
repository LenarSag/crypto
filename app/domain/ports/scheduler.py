# domain/ports/scheduler.py
from abc import ABC, abstractmethod
from typing import Awaitable, Callable


class IScheduler(ABC):
    """Abstract scheduler interface for periodic and one-off tasks."""

    @abstractmethod
    async def start(self) -> None:
        """Start the scheduler service."""

    @abstractmethod
    async def stop(self) -> None:
        """Stop the scheduler service."""

    @abstractmethod
    async def schedule_interval(
        self,
        name: str,
        interval_seconds: int,
        task: Callable[[], Awaitable[None]],
    ) -> None:
        """Schedule a recurring async task."""

    @abstractmethod
    async def cancel(self, name: str) -> None:
        """Cancel a scheduled task by its name/id."""
