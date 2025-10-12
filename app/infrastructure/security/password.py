from passlib.context import CryptContext

from app.domain.ports.pw_hasher import PasswordHasher

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class BCryptPasswordHasher(PasswordHasher):
    def hash(self, raw_password: str) -> str:
        return pwd_context.hash(raw_password)

    def verify(self, raw_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(raw_password, hashed_password)
