from typing import List
from uuid import UUID, uuid4

from app.domain.entities.subscription import (
    ComparisonOperator,
    Subscription,
    SubscriptionUpdate,
)
from app.domain.exceptions.subscription import SubscriptionNotFoundError
from app.domain.repositories.subscription_repo import ISubscriptionRepository


class SubscriptionService:
    """Business logic for managing subscriptions."""

    def __init__(self, subscription_repo: ISubscriptionRepository):
        self._repo = subscription_repo

    async def create_subscription(
        self,
        user_id: UUID,
        coin_id: UUID,
        threshold_value: float,
        comparison_operator: ComparisonOperator,
    ) -> Subscription:
        """Add a new subscription for a user watching a coin."""

        subscription = Subscription(
            id=uuid4(),
            user_id=user_id,
            coin_id=coin_id,
            threshold_value=threshold_value,
            comparison_operator=comparison_operator,
            is_active=True,
        )
        await self._repo.add(subscription)
        return subscription

    async def get_subscription_by_id(self, subscription_id: UUID) -> Subscription:
        """Retrieve a subscription by its ID. Raises SubscriptionNotFoundError if not found."""

        subscription = await self._repo.get_by_id(subscription_id)
        if not subscription:
            raise SubscriptionNotFoundError()
        return subscription

    async def update_subscription(
        self,
        subscription_id: UUID,
        update_data: SubscriptionUpdate,
    ):
        """Update subscription fields. Only non-None parameters will be updated."""

        subscription = await self._repo.get_by_id(subscription_id)
        if not subscription:
            raise SubscriptionNotFoundError()

        values_to_update = update_data.to_update_dict()

        updated_subscription = await self._repo.update(
            subscription_id, values_to_update
        )

        return updated_subscription

    async def list_user_subscriptions(
        self, user_id: UUID, active_only: bool = True
    ) -> List[Subscription]:
        """Return all subscriptions for a given user."""

        return await self._repo.list_by_user(user_id, active_only=active_only)

    async def list_coin_subscriptions(
        self, coin_id: UUID, active_only: bool = True
    ) -> List[Subscription]:
        """Return all subscriptions watching a specific coin."""

        return await self._repo.list_by_coin(coin_id, active_only=active_only)

    async def deactivate_subscription(self, subscription_id: UUID) -> None:
        """Soft delete: mark subscription as inactive."""

        subscription = await self._repo.get_by_id(subscription_id)
        if not subscription:
            raise SubscriptionNotFoundError()
        await self._repo.soft_delete(subscription_id)

    async def delete_subscription(self, subscription_id: UUID) -> None:
        """Delete a subscription by its ID from storage"""

        subscription = await self._repo.get_by_id(subscription_id)
        if not subscription:
            raise SubscriptionNotFoundError()
        await self._repo.delete_permanently(subscription_id)
