from app.domain.entities.subscription import Subscription
from app.infrastructure.models.subscriptions import Subscription as SubscriptionModel


class SubscriptionMapper:
    """Maps between SQLAlchemy SubscriptionModel and domain Subscription entity."""

    @staticmethod
    def to_entity(model: SubscriptionModel) -> Subscription:
        return Subscription(
            id=model.id,
            user_id=model.user_id,
            coin_id=model.coin_id,
            threshold_value=model.threshold_value,
            comparison_operator=model.comparsion_operator,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def to_model(entity: Subscription) -> SubscriptionModel:
        return SubscriptionModel(
            id=entity.id,
            user_id=entity.user_id,
            coin_id=entity.coin_id,
            threshold_value=entity.threshold_value,
            comparsion_operator=entity.comparison_operator,
            is_active=entity.is_active,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
