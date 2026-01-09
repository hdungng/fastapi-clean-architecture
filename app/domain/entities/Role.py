from dataclasses import dataclass


@dataclass
class Role:
    Id: int | None
    Name: str
    Description: str | None = None
    IsActive: bool = True
