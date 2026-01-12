from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from app.infrastructure.db.base import Base
from app.infrastructure.db.audit_mixin import AuditMixin


class RefreshTokenModel(AuditMixin, Base):
    __tablename__ = "RefreshTokens"

    id = Column("Id", Integer, primary_key=True, index=True)
    user_id = Column("UserId", Integer, ForeignKey("Users.Id", ondelete="CASCADE"), nullable=False)
    token = Column("Token", String(512), nullable=False, unique=True)
    expires_at = Column("ExpiresAt", DateTime(timezone=True), nullable=False)
    revoked_at = Column("RevokedAt", DateTime(timezone=True), nullable=True)
    replaced_by_token = Column("ReplacedByToken", String(512), nullable=True)
    is_revoked = Column("IsRevoked", Boolean, nullable=False, default=False)
