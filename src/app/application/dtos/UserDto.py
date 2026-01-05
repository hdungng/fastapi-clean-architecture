from typing import List, Optional
from pydantic import BaseModel, EmailStr


class UserDto(BaseModel):
    Id: int | None = None
    UserName: str
    Email: EmailStr
    FullName: str | None = None
    IsActive: bool = True
    Roles: Optional[List[str]] = None
    Permissions: Optional[List[str]] = None
