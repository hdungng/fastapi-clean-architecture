from dataclasses import dataclass


@dataclass
class Permission:
    Id: int | None
    Name: str
    Description: str | None = None
    IsActive: bool = True
