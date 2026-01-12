from typing import List, Optional
from pydantic import BaseModel, EmailStr


class UserDto(BaseModel):
    id: int | None = None
    user_name: str
    email: EmailStr
    full_name: str | None = None
    is_active: bool = True
    roles: Optional[List[str]] = None
