from redis.asyncio import Redis, from_url

from app.infrastructure.config.settings import settings

redis: Redis = from_url(settings.redis_url)


async def get_redis() -> Redis:
    """FastAPI dependency to get the Redis client."""

    return redis
