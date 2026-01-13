from dataclasses import dataclass


@dataclass
class Product:
    name: str
    price: float
    id: int | None = None
    is_active: bool = True
