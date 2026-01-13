from dataclasses import dataclass


@dataclass
class User:
    user_name: str
    email: str
    id: int | None = None
    full_name: str | None = None
    is_active: bool = True
    password_hash: str | None = None
