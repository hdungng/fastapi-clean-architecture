from pydantic import BaseModel


class ProductDto(BaseModel):
    Id: int | None = None
    Name: str
    Price: float
    IsActive: bool = True
