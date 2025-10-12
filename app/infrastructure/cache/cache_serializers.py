from dataclasses import asdict
from datetime import datetime
from uuid import UUID

from app.domain.entities.coin import Coin
from app.domain.entities.price import Price
from app.domain.entities.user import User, UserRole


class UserSerializer:
    """Serialize and deserialize User objects for caching."""

    @staticmethod
    def serialize(user: User) -> dict:
        data = asdict(user)
        data['id'] = str(user.id)
        data['role'] = user.role.value
        data['created_at'] = user.created_at.isoformat()
        return data

    @staticmethod
    def deserialize(data: dict) -> User:
        return User(
            id=UUID(data['id']),
            username=data['username'],
            email=data['email'],
            hashed_password=data['hashed_password'],
            telegram_id=data.get('telegram_id'),
            role=UserRole(data['role']),
            is_active=data['is_active'],
            created_at=datetime.fromisoformat(data['created_at']),
        )


class CoinSerializer:
    """Serialize and deserialize Coin objects for caching."""

    @staticmethod
    def serialize(user: Coin) -> dict:
        data = asdict(user)
        data['id'] = str(user.id)
        data['created_at'] = user.created_at.isoformat()
        return data

    @staticmethod
    def deserialize(data: dict) -> Coin:
        return Coin(
            id=UUID(data['id']),
            ticker=data['ticker'],
            name=data['name'],
            description=data['description'],
            created_at=datetime.fromisoformat(data['created_at']),
        )


class PriceSerializer:
    """Serialize and deserialize Coin objects for caching."""

    @staticmethod
    def serialize(price: Price) -> dict:
        data = asdict(price)
        data['id'] = str(price.id)
        data['coin_id'] = str(price.coin_id)
        data['timestamp'] = price.timestamp.isoformat()
        return data

    @staticmethod
    def deserialize(data: dict) -> Price:
        return Price(
            id=UUID(data['id']),
            coin_id=UUID(data['coind_id']),
            price=data['name'],
            timestamp=datetime.fromisoformat(data['created_at']),
        )
