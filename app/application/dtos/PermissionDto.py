from pydantic import BaseModel


class PermissionDto(BaseModel):
    id: int | None = None
    name: str
    description: str | None = None
    is_active: bool = True
