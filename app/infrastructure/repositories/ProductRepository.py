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
        row = self._session.query(ProductModel).filter(ProductModel.id == id).first()
        return self._MapToEntity(row) if row else None

    async def Add(self, entity: Product) -> Product:
        row = self._MapToModel(entity)
        self._session.add(row)
        self._session.flush()
        entity.id = row.id
        return entity

    async def Update(self, entity: Product) -> Product:
        row = self._session.query(ProductModel).filter(ProductModel.id == entity.id).first()
        if not row:
            raise KeyError("Product not found")
        row.name = entity.name
        row.price = entity.price
        row.is_active = entity.is_active
        self._session.flush()
        return entity

    async def Delete(self, id: int) -> None:
        row = self._session.query(ProductModel).filter(ProductModel.id == id).first()
        if row:
            self._session.delete(row)
            self._session.flush()

    def _MapToEntity(self, row: ProductModel) -> Product:
        return Product(
            id=row.id,
            name=row.name,
            price=row.price,
            is_active=row.is_active,
        )

    def _MapToModel(self, entity: Product) -> ProductModel:
        return ProductModel(
            id=entity.id,
            name=entity.name,
            price=entity.price,
            is_active=entity.is_active,
        )
