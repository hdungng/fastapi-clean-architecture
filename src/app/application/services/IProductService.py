from abc import ABC, abstractmethod
from typing import List, Optional

from app.application.dtos.ProductDto import ProductDto


class IProductService(ABC):
    @abstractmethod
    async def GetAll(self) -> List[ProductDto]:
        pass

    @abstractmethod
    async def GetById(self, id: int) -> Optional[ProductDto]:
        pass

    @abstractmethod
    async def Create(self, dto: ProductDto) -> ProductDto:
        pass

    @abstractmethod
    async def Update(self, id: int, dto: ProductDto) -> ProductDto:
        pass

    @abstractmethod
    async def Delete(self, id: int) -> None:
        pass
