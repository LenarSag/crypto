from domain.entities.user import User

from app.infrastructure.models.users import User as UserModel


class UserMapper:
    """Maps between SQLAlchemy UserModel and domain User entity."""

    @staticmethod
    def to_entity(model: UserModel) -> User:
        return User(
            id=model.id,
            username=model.username,
            email=model.email,
            hashed_password=model.hashed_password,
            telegram_id=model.telegram_id,
            role=model.role,
            is_active=model.is_active,
            created_at=model.created_at,
        )

    @staticmethod
    def to_model(entity: User) -> UserModel:
        return UserModel(
            id=entity.id,
            username=entity.username,
            email=entity.email,
            hashed_password=entity.hashed_password,
            telegram_id=entity.telegram_id,
            role=entity.role,
            is_active=entity.is_active,
            created_at=entity.created_at,
        )
