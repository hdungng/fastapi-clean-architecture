from dataclasses import dataclass
from typing import List, Optional


@dataclass
class User:
    id: int | None
    user_name: str
    email: str
    full_name: str | None = None
    is_active: bool = True
    password_hash: str | None = None
