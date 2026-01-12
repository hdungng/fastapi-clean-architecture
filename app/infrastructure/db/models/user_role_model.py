from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from app.infrastructure.db.base import Base
from app.infrastructure.db.audit_mixin import AuditMixin


class UserRoleModel(AuditMixin, Base):
    __tablename__ = "UserRoles"

    id = Column("Id", Integer, primary_key=True, index=True)
    user_id = Column("UserId", Integer, ForeignKey("Users.Id", ondelete="CASCADE"), nullable=False)
    role_id = Column("RoleId", Integer, ForeignKey("Roles.Id", ondelete="CASCADE"), nullable=False)

    __table_args__ = (UniqueConstraint("UserId", "RoleId", name="uq_user_role"),)
