from typing import List, Optional
from sqlalchemy.orm import Session

from app.domain.repositories.IProductRepository import IProductRepository
from app.domain.entities.Product import Product
from app.infrastructure.db.models.product_model import ProductModel


class ProductRepository(IProductRepository):
    def __init__(self, session: Session):
        self._session = session

    async def GetAll(self) -> List[Product]:
        rows = self._session.query(ProductModel).all()
        return [self._MapToEntity(r) for r in rows]

    async def GetById(self, id: int) -> Optional[Product]:
        row = self._session.query(ProductModel).filter(ProductModel.Id == id).first()
        return self._MapToEntity(row) if row else None

    async def Add(self, entity: Product) -> Product:
        row = self._MapToModel(entity)
        self._session.add(row)
        self._session.flush()
        entity.Id = row.Id
        return entity

    async def Update(self, entity: Product) -> Product:
        row = self._session.query(ProductModel).filter(ProductModel.Id == entity.Id).first()
        if not row:
            raise KeyError("Product not found")
        row.Name = entity.Name
        row.Price = entity.Price
        row.IsActive = entity.IsActive
        self._session.flush()
        return entity

    async def Delete(self, id: int) -> None:
        row = self._session.query(ProductModel).filter(ProductModel.Id == id).first()
        if row:
            self._session.delete(row)
            self._session.flush()

    def _MapToEntity(self, row: ProductModel) -> Product:
        return Product(
            Id=row.Id,
            Name=row.Name,
            Price=row.Price,
            IsActive=row.IsActive,
        )

    def _MapToModel(self, entity: Product) -> ProductModel:
        return ProductModel(
            Id=entity.Id,
            Name=entity.Name,
            Price=entity.Price,
            IsActive=entity.IsActive,
        )
