from abc import ABC, abstractmethod
from typing import Optional


class IExternalPriceProvider(ABC):
    """Abstraction for fetching price data from external sources (API, feed, etc.)."""

    @abstractmethod
    async def fetch_current_price(self, ticker: str) -> Optional[float]:
        """Return the latest price value for a given coin ID."""

        pass
