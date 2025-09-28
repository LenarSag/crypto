from abc import ABC, abstractmethod


class PasswordHasher(ABC):
    """
    Domain-level contract for password hashing/verification.
    Implementations (bcrypt, argon2, etc.) live in infrastructure.
    """

    @abstractmethod
    def hash(self, raw_password: str) -> str: ...

    @abstractmethod
    def verify(self, raw_password: str, hashed_password: str) -> bool: ...
