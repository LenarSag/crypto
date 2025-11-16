from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.infrastructure.config.settings import settings
from app.infrastructure.models import Base

engine = create_async_engine(url=settings.postgres_url, echo=True)
# engine = create_async_engine(url=settings.test_db_url, echo=True)

async_session = async_sessionmaker(
    bind=engine, autoflush=False, autocommit=False, expire_on_commit=False
)


async def init_models():
    async with engine.begin() as conn:
        existing_tables = await conn.run_sync(Base.metadata.reflect)
        if not existing_tables:
            await conn.run_sync(Base.metadata.create_all)


async def get_session() -> AsyncIterator[AsyncSession]:
    async with async_session() as session:
        yield session
