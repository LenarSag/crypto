import json
from typing import Any, Optional

from redis.asyncio import Redis

from app.domain.ports.cache import ICache


class RedisCache(ICache):
    """Async Redis cache implementation of ICache."""

    def __init__(self, redis: Redis):
        self._redis = redis

    async def get(self, key: str) -> Optional[Any]:
        value = await self._redis.get(key)
        if value is None:
            return None
        value = json.loads(value)

        return value

    async def set(
        self, key: str, value: Any, expire_seconds: Optional[int] = None
    ) -> None:
        data = json.dumps(value, default=str)

        if expire_seconds:
            await self._redis.set(key, data, ex=expire_seconds)
        else:
            await self._redis.set(key, data)

    async def delete(self, key: str) -> None:
        await self._redis.delete(key)

    async def exists(self, key: str) -> bool:
        return bool(await self._redis.exists(key))
