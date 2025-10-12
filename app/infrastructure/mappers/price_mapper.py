from app.domain.entities.price import Price
from app.infrastructure.models.prices import Price as PriceModel


class PriceMapper:
    """Maps between SQLAlchemy PriceModel and domain Price entity."""

    @staticmethod
    def to_entity(model: PriceModel) -> Price:
        return Price(
            id=model.id,
            coin_id=model.coin_id,
            price=model.price,
            timestamp=model.timestamp,
        )

    @staticmethod
    def to_model(entity: Price) -> PriceModel:
        return PriceModel(
            id=entity.id,
            coin_id=entity.coin_id,
            price=entity.price,
            timestamp=entity.timestamp,
        )
