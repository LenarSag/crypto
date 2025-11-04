import asyncio
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.infrastructure.brokers.faststream_rabbit_broke import broker_service
from app.infrastructure.cache.redis_client import redis
from app.infrastructure.config.settings import settings
from app.infrastructure.db.database import init_models
from app.presentation.api.routes.users import user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Startup ---
    print('Starting FastAPI application...')

    await broker_service.start()
    print('RabbitMQ broker started')

    app.state.redis = redis
    await app.state.redis.ping()
    print('Redis connected')

    yield

    # --- Shutdown ---
    await broker_service.stop()
    print('RabbitMQ broker stopped')

    await app.state.redis.close()
    print('Redis connection closed')


app = FastAPI(lifespan=lifespan)

app.include_router(prefix=settings.MAIN_API_URL + '/users', router=user_router)


@app.get('/')
async def index():
    return {'message': 'Crypto Alert Service is running.'}


if __name__ == '__main__':
    asyncio.run(init_models())
    uvicorn.run(app='main:app', host=settings.HOST, port=settings.PORT, reload=True)
