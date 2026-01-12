from sqlalchemy import Column, Integer, String, Boolean
from app.infrastructure.db.base import Base
from app.infrastructure.db.audit_mixin import AuditMixin


class PermissionModel(AuditMixin, Base):
    __tablename__ = "Permissions"

    id = Column("Id", Integer, primary_key=True, index=True)
    name = Column("Name", String(150), nullable=False, unique=True)
    description = Column("Description", String(256), nullable=True)
    is_active = Column("IsActive", Boolean, nullable=False, default=True)
