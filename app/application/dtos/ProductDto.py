from pydantic import BaseModel


class ProductDto(BaseModel):
    id: int | None = None
    name: str
    price: float
    is_active: bool = True
