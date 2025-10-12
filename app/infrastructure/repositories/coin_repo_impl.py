from typing import Optional, Sequence
from uuid import UUID

from sqlalchemy import delete, func
from sqlalchemy import update as sql_update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import aliased, selectinload

from app.domain.const.constants import DEFAULT_LIMIT, DEFAULT_OFFSET
from app.domain.entities.coin import Coin
from app.domain.repositories.coin_repo import ICoinRepository
from app.infrastructure.mappers.coin_mapper import CoinMapper
from app.infrastructure.models.coins import Coin as CoinModel
from app.infrastructure.models.prices import Price as PriceModel


class SQLAlchemyCoinRepository(ICoinRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, coin: Coin) -> Coin:
        coin_model = CoinMapper.to_model(coin)
        self._session.add(coin_model)
        await self._session.commit()
        return coin

    async def get_by_id(self, coin_id: UUID) -> Optional[Coin]:
        stmt = select(CoinModel).filter_by(id=coin_id)
        result = await self._session.execute(stmt)
        coin_model = result.scalar()
        if coin_model:
            return CoinMapper.to_entity(coin_model)
        return None

    async def get_by_ticker(self, ticker: str) -> Optional[Coin]:
        stmt = select(CoinModel).filter_by(ticker=ticker)
        result = await self._session.execute(stmt)
        coin_model = result.scalar()
        if coin_model:
            return CoinMapper.to_entity(coin_model)
        return None

    async def get_by_name(self, name: str) -> Optional[Coin]:
        stmt = select(CoinModel).filter_by(name=name)
        result = await self._session.execute(stmt)
        coin_model = result.scalar()
        if coin_model:
            return CoinMapper.to_entity(coin_model)
        return None

    async def list_coins(
        self, offset: int = DEFAULT_OFFSET, limit: int = DEFAULT_LIMIT
    ) -> Sequence[Coin]:
        stmt = select(CoinModel).offset(offset).limit(limit)
        result = await self._session.execute(stmt)
        coin_models = result.scalars().all()
        coins_list = [CoinMapper.to_entity(coin_model) for coin_model in coin_models]
        return coins_list

    async def update(self, coin_id: UUID, update_data: dict) -> Coin:
        stmt = (
            sql_update(CoinModel).where(CoinModel.id == coin_id).values(**update_data)
        )
        await self._session.execute(stmt)
        await self._session.commit()

        result = await self._session.execute(
            select(CoinModel).where(CoinModel.id == coin_id)
        )
        coin_model = result.scalar()
        return CoinMapper.to_entity(coin_model)

    async def delete(self, coin_id: UUID) -> None:
        stmt = delete(CoinModel).where(CoinModel.id == coin_id)
        await self._session.execute(stmt)
        await self._session.commit()

    async def get_with_latest_price(self, coin_id: UUID) -> Optional[Coin]:
        query = (
            select(CoinModel)
            .options(
                selectinload(
                    CoinModel.prices.and_(
                        PriceModel.timestamp
                        == select(func.max(PriceModel.timestamp))
                        .where(PriceModel.coin_id == coin_id)
                        .scalar_subquery()
                    )
                )
            )
            .where(CoinModel.id == coin_id)
        )

        result = await self._session.execute(query)
        coin_model = result.scalar()
        if coin_model:
            coin = CoinMapper.to_entity(coin_model)
            coin.price = coin_model.prices[0].price if coin_model.prices else None
            return coin
        return None

    async def list_with_latest_prices(
        self, *, offset: int = DEFAULT_OFFSET, limit: int = DEFAULT_LIMIT
    ) -> Optional[list[Coin]]:
        latest_prices_subq = select(
            PriceModel,
            func.row_number()
            .over(partition_by=PriceModel.coin_id, order_by=PriceModel.timestamp.desc())
            .label('rn'),
        ).subquery()

        LatestPrice = aliased(PriceModel, latest_prices_subq)

        query = (
            select(CoinModel, LatestPrice)
            .join(LatestPrice, CoinModel.id == LatestPrice.coin_id)
            .where(LatestPrice.rn == 1)
            .order_by(CoinModel.ticker)
            .offset(offset)
            .limit(limit)
        )

        result = await self._session.execute(query)
        rows = result.all()

        coins = []
        for row in rows:
            coin_model, latest_price = row
            coin = CoinMapper.to_entity(coin_model)
            coin.price = latest_price.price if latest_price else None
            coins.append(coin)
        return coins
