from dataclasses import dataclass


@dataclass
class Product:
    id: int | None
    name: str
    price: float
    is_active: bool = True
