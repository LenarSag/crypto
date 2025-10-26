from typing import Optional, Sequence
from uuid import UUID

from sqlalchemy import delete
from sqlalchemy import update as sql_update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.domain.entities.subscription import Subscription
from app.domain.repositories.subscription_repo import ISubscriptionRepository
from app.infrastructure.mappers.subscription_mapper import SubscriptionMapper
from app.infrastructure.models.subscriptions import Subscription as SubscriptionModel


class SqlAlchemySubscriptionRepository(ISubscriptionRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, subscription: Subscription) -> Subscription:
        subscription_model = SubscriptionMapper.to_model(subscription)
        self._session.add(subscription_model)
        await self._session.commit()
        return subscription

    async def get_by_id(self, subscription_id: UUID) -> Optional[Subscription]:
        stmt = select(SubscriptionModel).filter_by(id=subscription_id)
        result = await self._session.execute(stmt)
        subscription_model = result.scalar()
        if subscription_model:
            return SubscriptionMapper.to_entity(subscription_model)
        return None

    async def list_by_user(
        self, user_id: UUID, *, active_only: bool = True
    ) -> Sequence[Subscription]:
        stmt = select(SubscriptionModel).filter_by(
            user_id=user_id, active_only=active_only
        )
        result = await self._session.execute(stmt)
        subscription_models = result.scalars().all()
        subscriptions_list = [
            SubscriptionMapper.to_entity(subscription_model)
            for subscription_model in subscription_models
        ]
        return subscriptions_list

    async def list_by_coin(
        self, coin_id: UUID, *, active_only: bool = True
    ) -> Sequence[Subscription]:
        stmt = select(SubscriptionModel).filter_by(
            coin_id=coin_id, active_only=active_only
        )
        result = await self._session.execute(stmt)
        subscription_models = result.scalars().all()
        subscriptions_list = [
            SubscriptionMapper.to_entity(subscription_model)
            for subscription_model in subscription_models
        ]
        return subscriptions_list

    async def update(
        self,
        subscription_id: UUID,
        update_data: dict,
    ) -> Subscription:
        stmt = (
            sql_update(SubscriptionModel)
            .where(SubscriptionModel.id == subscription_id)
            .values(**update_data)
            .returning(SubscriptionModel)
        )
        result = await self._session.execute(stmt)
        await self._session.commit()

        updated_model = result.scalar()
        return SubscriptionMapper.to_entity(updated_model)

    async def soft_delete(self, subscription_id: UUID) -> None:
        stmt = (
            sql_update(SubscriptionModel)
            .where(SubscriptionModel.id == subscription_id)
            .values(is_active=False)
        )
        await self._session.execute(stmt)
        await self._session.commit()

    async def delete_permanently(self, subscription_id: UUID) -> None:
        stmt = delete(SubscriptionModel).where(SubscriptionModel.id == subscription_id)
        await self._session.execute(stmt)
        await self._session.commit()
