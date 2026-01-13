from pydantic import BaseModel


class ProductCreateDto(BaseModel):
    name: str
    price: float
    is_active: bool = True
