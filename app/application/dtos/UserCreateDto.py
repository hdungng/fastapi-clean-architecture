from typing import List, Optional
from pydantic import BaseModel, EmailStr


class UserCreateDto(BaseModel):
    user_name: str
    email: EmailStr
    full_name: str | None = None
    is_active: bool = True
    password: str
    roles: Optional[List[str]] = None
