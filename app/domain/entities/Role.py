from dataclasses import dataclass


@dataclass
class Role:
    name: str
    id: int | None = None
    description: str | None = None
    is_active: bool = True
