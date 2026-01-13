from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from app.infrastructure.db.base import Base
from app.infrastructure.db.audit_mixin import AuditMixin


class UserRoleModel(AuditMixin, Base):
    __tablename__ = "user_roles"

    id = Column("id", Integer, primary_key=True, index=True)
    user_id = Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    role_id = Column("role_id", Integer, ForeignKey("roles.id", ondelete="CASCADE"), nullable=False)

    __table_args__ = (UniqueConstraint("user_id", "role_id", name="uq_user_role"),)
