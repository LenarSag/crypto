import json
from typing import Any, Optional

from redis.asyncio import Redis

from app.domain.ports.cache import ICache


class RedisCache(ICache):
    """Async Redis cache implementation of ICache."""

    def __init__(self, redis: Redis):
        self._redis = redis

    async def get(self, key: str) -> Optional[Any]:
        async with self._redis.client() as client:
            value = await client.get(key)
            if value is None:
                return None
            value = json.loads(value)

            return value

    async def set(
        self, key: str, value: Any, expire_seconds: Optional[int] = None
    ) -> None:
        data = json.dumps(value, default=str)

        async with self._redis.client() as client:
            if expire_seconds:
                await client.set(key, data, ex=expire_seconds)
            else:
                await client.set(key, data)

    async def delete(self, key: str) -> None:
        async with self._redis.client() as client:
            await client.delete(key)

    async def exists(self, key: str) -> bool:
        async with self._redis.client() as client:
            return bool(await client.exists(key))
