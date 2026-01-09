from typing import List, Optional

from app.application.dtos.ProductDto import ProductDto
from app.application.services.interfaces.IProductService import IProductService
from app.domain.entities.Product import Product
from app.domain.repositories.IUnitOfWork import IUnitOfWork
from app.infrastructure.mapping.AutoMapper import MapperInstance


class ProductService(IProductService):
    """Service xử lý logic cho Product."""

    def __init__(self, unit_of_work: IUnitOfWork):
        self._unit_of_work = unit_of_work

    async def GetAll(self) -> List[ProductDto]:
        entities = await self._unit_of_work.Products.GetAll()
        return [MapperInstance.Map(e, ProductDto) for e in entities]

    async def GetById(self, id: int) -> Optional[ProductDto]:
        entity = await self._unit_of_work.Products.GetById(id)
        return MapperInstance.Map(entity, ProductDto) if entity else None

    async def Create(self, dto: ProductDto) -> ProductDto:
        entity = MapperInstance.Map(dto, Product)
        created = await self._unit_of_work.Products.Add(entity)
        await self._unit_of_work.SaveChanges()
        return MapperInstance.Map(created, ProductDto)

    async def Update(self, id: int, dto: ProductDto) -> ProductDto:
        entity = MapperInstance.Map(dto, Product)
        entity.Id = id
        updated = await self._unit_of_work.Products.Update(entity)
        await self._unit_of_work.SaveChanges()
        return MapperInstance.Map(updated, ProductDto)

    async def Delete(self, id: int) -> None:
        await self._unit_of_work.Products.Delete(id)
        await self._unit_of_work.SaveChanges()
