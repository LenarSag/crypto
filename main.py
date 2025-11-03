from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.infrastructure.brokers.faststream_rabbit_broke import FastStreamRabbitBroker
from app.infrastructure.cache.redis_client import redis
from app.infrastructure.config.settings import settings

broker_service = FastStreamRabbitBroker(settings.rabbitmq_url)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Startup ---
    print('Starting FastAPI application...')

    await broker_service.start()
    print('RabbitMQ broker started')

    await redis.ping()
    print('Redis connected')

    yield

    # --- Shutdown ---
    await broker_service.stop()
    print('RabbitMQ broker stopped')

    await redis.close()
    print('Redis connection closed')


app = FastAPI(lifespan=lifespan)

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000, reload=True)
