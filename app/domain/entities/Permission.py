from dataclasses import dataclass


@dataclass
class Permission:
    name: str
    id: int | None = None
    description: str | None = None
    is_active: bool = True
