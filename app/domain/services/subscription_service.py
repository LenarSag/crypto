from datetime import datetime, timezone
from typing import List
from uuid import UUID

from app.domain.entities.subscription import ComparisonOperator, Subscription
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
            id=0,
            user_id=user_id,
            coin_id=coin_id,
            threshold_value=threshold_value,
            comparison_operator=comparison_operator,
            is_active=True,
        )
        await self._repo.add(subscription)
        return subscription

    async def get_sunbscription_by_id(self, subscription_id: int) -> Subscription:
        """Retrieve a subscription by its ID. Raises SubscriptionNotFoundError if not found."""

        subscription = await self._repo.get_by_id(subscription_id)
        if not subscription:
            raise SubscriptionNotFoundError(subscription_id)
        return subscription

    async def update_subscription(
        self,
        subscription_id: int,
        threshold_value: float,
        comparison_operator: ComparisonOperator,
    ):
        """
        Update subscription fields. Only non-None parameters will be updated.
        Raises SubscriptionNotFoundError if the subscription does not exist.
        """
        subscription = await self._repo.get_by_id(subscription_id)
        if not subscription:
            raise SubscriptionNotFoundError(subscription_id)

        subscription.threshold_value = threshold_value
        subscription.comparison_operator = comparison_operator
        subscription.updated_at = datetime.now(timezone.utc)
        await self._repo.update(subscription)

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

    async def delete_subscription(self, subscription_id: int) -> None:
        """Delete a subscription by its ID. Raises SubscriptionNotFoundError if not found."""

        subscription = await self._repo.get_by_id(subscription_id)
        if not subscription:
            raise SubscriptionNotFoundError(subscription_id)
        await self._repo.delete(subscription_id)
