from sqlalchemy import Column, Integer, String, Boolean, Float
from app.infrastructure.db.base import Base
from app.infrastructure.db.audit_mixin import AuditMixin


class ProductModel(AuditMixin, Base):
    __tablename__ = "products"

    id = Column("id", Integer, primary_key=True, index=True)
    name = Column("name", String(256), nullable=False)
    price = Column("price", Float, nullable=False)
    is_active = Column("is_active", Boolean, nullable=False, default=True)
