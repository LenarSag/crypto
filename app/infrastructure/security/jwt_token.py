from datetime import datetime, timedelta, timezone
from uuid import UUID

import jwt
from jwt.exceptions import InvalidTokenError as JWTInvalidTokenError

from app.domain.exceptions.token import (
    InvalidTokenError,
    TokenExpiredError,
)
from app.domain.ports.token_provider import TokenProvider
from app.infrastructure.config.settings import settings


class JWTTokenProvider(TokenProvider):
    def create_access_token(self, user_id: UUID) -> str:
        to_encode = {'sub': str(user_id)}
        expire = datetime.now() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode.update({'exp': expire})
        encoded_jwt = jwt.encode(
            to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
        )
        return encoded_jwt

    def verify_token(self, access_token: str) -> UUID | None:
        try:
            payload = jwt.decode(
                access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
        except JWTInvalidTokenError:
            raise InvalidTokenError

        user_id = payload.get('sub')
        if user_id is None:
            raise InvalidTokenError

        expire = payload.get('exp')
        if expire is None:
            raise InvalidTokenError
        try:
            expiring_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
        except ValueError:
            raise InvalidTokenError
        if expiring_time < datetime.now(timezone.utc):
            raise TokenExpiredError

        return user_id
