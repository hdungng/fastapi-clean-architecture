from pydantic import BaseModel


class RoleDto(BaseModel):
    Id: int | None = None
    Name: str
    Description: str | None = None
    IsActive: bool = True
