from pydantic import BaseModel


class PermissionCreateDto(BaseModel):
    name: str
    description: str | None = None
    is_active: bool = True
