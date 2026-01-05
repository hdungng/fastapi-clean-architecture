from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities.Product import Product


class IProductRepository(ABC):
    @abstractmethod
    async def GetAll(self) -> List[Product]:
        pass

    @abstractmethod
    async def GetById(self, id: int) -> Optional[Product]:
        pass

    @abstractmethod
    async def Add(self, entity: Product) -> Product:
        pass

    @abstractmethod
    async def Update(self, entity: Product) -> Product:
        pass

    @abstractmethod
    async def Delete(self, id: int) -> None:
        pass
