from datetime import datetime, timedelta, timezone
from uuid import UUID

import jwt
from jwt.exceptions import InvalidTokenError

from app.domain.ports.token_provider import TokenProvider
from app.infrastructure.const.constants import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    SECRET_KEY,
)
from app.infrastructure.exceptions.token_exceptions import (
    InvalidTokenException,
    TokenExpiredException,
)


class JWTTokenProvider(TokenProvider):
    def create_access_token(self, user_id: UUID) -> str:
        to_encode = {'sub': str(user_id)}
        expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({'exp': expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def verify_token(self, access_token: str) -> UUID | None:
        try:
            payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        except InvalidTokenError:
            raise InvalidTokenException

        user_id = payload.get('sub')
        if user_id is None:
            raise InvalidTokenException

        expire = payload.get('exp')
        if expire is None:
            raise InvalidTokenException
        try:
            expiring_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
        except ValueError:
            raise InvalidTokenError
        if expiring_time < datetime.now(timezone.utc):
            raise TokenExpiredException

        return user_id
