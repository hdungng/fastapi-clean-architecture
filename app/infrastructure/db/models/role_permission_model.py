from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from app.infrastructure.db.base import Base
from app.infrastructure.db.audit_mixin import AuditMixin


class RolePermissionModel(AuditMixin, Base):
    __tablename__ = "role_permissions"

    id = Column("id", Integer, primary_key=True, index=True)
    role_id = Column("role_id", Integer, ForeignKey("roles.id", ondelete="CASCADE"), nullable=False)
    permission_id = Column("permission_id", Integer, ForeignKey("permissions.id", ondelete="CASCADE"), nullable=False)

    __table_args__ = (UniqueConstraint("role_id", "permission_id", name="uq_role_permission"),)
