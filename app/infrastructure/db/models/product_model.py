from sqlalchemy import Column, Integer, String, Boolean, Float
from app.infrastructure.db.base import Base
from app.infrastructure.db.audit_mixin import AuditMixin


class ProductModel(AuditMixin, Base):
    __tablename__ = "Products"

    id = Column("Id", Integer, primary_key=True, index=True)
    name = Column("Name", String(256), nullable=False)
    price = Column("Price", Float, nullable=False)
    is_active = Column("IsActive", Boolean, nullable=False, default=True)
