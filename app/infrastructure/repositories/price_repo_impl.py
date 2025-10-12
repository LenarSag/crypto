from datetime import datetime
from typing import Optional, Sequence
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.domain.const.constants import DEFAULT_LIMIT, DEFAULT_OFFSET
from app.domain.entities.price import Price
from app.domain.repositories.price_repo import IPriceRepository
from app.infrastructure.mappers.price_mapper import PriceMapper
from app.infrastructure.models.prices import Price as PriceModel


class SQLAlchemyPriceRepository(IPriceRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, price: Price) -> Price:
        price_model = PriceMapper.to_model(price)
        self._session.add(price_model)
        await self._session.commit()
        return price

    async def list_by_coin(
        self,
        coin_id: UUID,
        *,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        offset: int = DEFAULT_OFFSET,
        limit: int = DEFAULT_LIMIT,
    ) -> Sequence[Price]:
        stmt = select(PriceModel).filter_by(coin_id=coin_id)

        if start_date:
            stmt = stmt.filter(PriceModel.timestamp >= start_date)
        if end_date:
            stmt = stmt.filter(PriceModel.timestamp <= end_date)

        stmt = stmt.offset(offset).limit(limit)
        result = await self._session.execute(stmt)
        price_models = result.scalars().all()
        prices_list = [
            PriceMapper.to_entity(price_model) for price_model in price_models
        ]
        return prices_list

    async def get_latest(self, coin_id: UUID) -> Optional[Price]:
        stmt = (
            select(PriceModel)
            .filter_by(coin_id=coin_id)
            .order_by(PriceModel.timestamp.desc())
            .limit(1)
        )
        result = await self._session.execute(stmt)
        price_model = result.scalar()
        if price_model:
            return PriceMapper.to_entity(price_model)
        return None
