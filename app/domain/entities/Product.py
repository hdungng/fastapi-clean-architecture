from dataclasses import dataclass


@dataclass
class Product:
    Id: int | None
    Name: str
    Price: float
    IsActive: bool = True
