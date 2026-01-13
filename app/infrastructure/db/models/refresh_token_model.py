from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from app.infrastructure.db.base import Base
from app.infrastructure.db.audit_mixin import AuditMixin


class RefreshTokenModel(AuditMixin, Base):
    __tablename__ = "refresh_tokens"

    id = Column("id", Integer, primary_key=True, index=True)
    user_id = Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    token = Column("token", String(512), nullable=False, unique=True)
    expires_at = Column("expires_at", DateTime(timezone=True), nullable=False)
    revoked_at = Column("revoked_at", DateTime(timezone=True), nullable=True)
    replaced_by_token = Column("replaced_by_token", String(512), nullable=True)
    is_revoked = Column("is_revoked", Boolean, nullable=False, default=False)
