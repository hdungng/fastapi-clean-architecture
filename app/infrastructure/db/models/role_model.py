from sqlalchemy import Column, Integer, String, Boolean
from app.infrastructure.db.base import Base
from app.infrastructure.db.audit_mixin import AuditMixin


class RoleModel(AuditMixin, Base):
    __tablename__ = "Roles"

    id = Column("Id", Integer, primary_key=True, index=True)
    name = Column("Name", String(100), nullable=False, unique=True)
    description = Column("Description", String(256), nullable=True)
    is_active = Column("IsActive", Boolean, nullable=False, default=True)
