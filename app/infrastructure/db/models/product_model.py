from sqlalchemy import Column, Integer, String, Boolean, Float
from app.infrastructure.db.base import Base
from app.infrastructure.db.audit_mixin import AuditMixin


class ProductModel(AuditMixin, Base):
    __tablename__ = "Products"

    Id = Column(Integer, primary_key=True, index=True)
    Name = Column(String(256), nullable=False)
    Price = Column(Float, nullable=False)
    IsActive = Column(Boolean, nullable=False, default=True)
