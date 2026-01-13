from pydantic import BaseModel


class RoleCreateDto(BaseModel):
    name: str
    description: str | None = None
    is_active: bool = True
