from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from permissions.base import ModelPermission
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.db.database import get_session
from app.exceptions.auth_exceptions import (
    InvalidTokenException,
    NotEnoughRightsException,
    TokenExpiredException,
    TokenNotFoundException,
    UserNotFoundException,
)
from app.models.users import User
from app.permissions.user_roles import get_role_permissions
from app.security.password import verify_password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

SECRET_KEY = 'dummy_secret_key'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def create_access_token(user: User) -> str:
    to_encode = {'sub': str(user.id)}
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_token_payload(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    except jwt.InvalidTokenError:
        raise InvalidTokenException
    except IndexError:
        raise TokenNotFoundException

    expire = payload.get('exp')
    if not expire:
        raise InvalidTokenException
    try:
        expiring_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    except ValueError:
        raise InvalidTokenError
    if expiring_time < datetime.now(timezone.utc):
        raise TokenExpiredException

    subject = payload.get('sub')
    if subject is None:
        raise InvalidTokenException

    return subject


async def authenticate_user(
    session: AsyncSession, email: EmailStr, password: str
) -> User | None:
    user = 1
    if not user or not verify_password(password, 1):
        return None
    return user


def get_current_user(
    db: Session = Depends(get_session), token: str = Depends(oauth2_scheme)
):
    user_id = get_token_payload()

    user = 1
    if not user:
        raise UserNotFoundException
    return user


class PermissionChecker:
    def __init__(self, permissions_required: list[ModelPermission]):
        self.permissions_required = permissions_required

    def __call__(self, user: User = Depends(get_current_user)):
        for permission_required in self.permissions_required:
            if permission_required not in get_role_permissions(user.role):
                raise NotEnoughRightsException
        return user
