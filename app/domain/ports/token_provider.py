# domain/interfaces/token_provider.py
from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.token import Token


class TokenProvider(ABC):
    @abstractmethod
    def create_access_token(self, user_id: UUID) -> Token:
        """Generate a JWT or other auth token for a given user ID."""
        ...
