from passlib.context import CryptContext

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def HashPassword(password: str) -> str:
    return _pwd_context.hash(password)


def VerifyPassword(plain_password: str, hashed_password: str | None) -> bool:
    if hashed_password is None:
        return False
    return _pwd_context.verify(plain_password, hashed_password)
