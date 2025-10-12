from app.domain.entities.coin import Coin
from app.infrastructure.models.coins import Coin as CoinModel


class CoinMapper:
    """Maps between SQLAlchemy CoinModel and domain Coin entity."""

    @staticmethod
    def to_entity(model: CoinModel) -> Coin:
        return Coin(
            id=model.id,
            ticker=model.ticker,
            name=model.name,
            description=model.description,
            created_at=model.created_at,
        )

    @staticmethod
    def to_model(entity: Coin) -> CoinModel:
        return CoinModel(
            id=entity.id,
            ticker=entity.ticker,
            name=entity.name,
            description=entity.description,
            created_at=entity.created_at,
        )
