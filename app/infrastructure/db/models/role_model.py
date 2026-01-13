from sqlalchemy import Column, Integer, String, Boolean
from app.infrastructure.db.base import Base
from app.infrastructure.db.audit_mixin import AuditMixin


class RoleModel(AuditMixin, Base):
    __tablename__ = "roles"

    id = Column("id", Integer, primary_key=True, index=True)
    name = Column("name", String(100), nullable=False, unique=True)
    description = Column("description", String(256), nullable=True)
    is_active = Column("is_active", Boolean, nullable=False, default=True)
