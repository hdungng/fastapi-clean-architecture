from dataclasses import dataclass
from typing import List, Optional


@dataclass
class User:
    Id: int | None
    UserName: str
    Email: str
    FullName: str | None = None
    IsActive: bool = True
    PasswordHash: str | None = None
    Roles: Optional[List[str]] = None
    Permissions: Optional[List[str]] = None
