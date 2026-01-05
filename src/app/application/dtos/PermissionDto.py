from pydantic import BaseModel


class PermissionDto(BaseModel):
    Id: int | None = None
    Name: str
    Description: str | None = None
    IsActive: bool = True
