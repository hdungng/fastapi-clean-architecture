from sqlalchemy import Column, Integer, String, Boolean
from app.infrastructure.db.base import Base
from app.infrastructure.db.audit_mixin import AuditMixin


class RoleModel(AuditMixin, Base):
    __tablename__ = "Roles"

    Id = Column(Integer, primary_key=True, index=True)
    Name = Column(String(100), nullable=False, unique=True)
    Description = Column(String(256), nullable=True)
    IsActive = Column(Boolean, nullable=False, default=True)
