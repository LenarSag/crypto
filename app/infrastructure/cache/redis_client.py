from redis.asyncio import Redis, from_url

REDIS_URL = 'redis://localhost:6379'


redis: Redis = from_url(
    REDIS_URL,
    decode_responses=True,
)


async def get_redis() -> Redis:
    """FastAPI dependency to get the Redis client."""

    return redis
