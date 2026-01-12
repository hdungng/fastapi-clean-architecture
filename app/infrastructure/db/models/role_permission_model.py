from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from app.infrastructure.db.base import Base
from app.infrastructure.db.audit_mixin import AuditMixin


class RolePermissionModel(AuditMixin, Base):
    __tablename__ = "RolePermissions"

    id = Column("Id", Integer, primary_key=True, index=True)
    role_id = Column("RoleId", Integer, ForeignKey("Roles.Id", ondelete="CASCADE"), nullable=False)
    permission_id = Column("PermissionId", Integer, ForeignKey("Permissions.Id", ondelete="CASCADE"), nullable=False)

    __table_args__ = (UniqueConstraint("RoleId", "PermissionId", name="uq_role_permission"),)
