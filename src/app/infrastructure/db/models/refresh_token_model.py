from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from app.infrastructure.db.base import Base
from app.infrastructure.db.audit_mixin import AuditMixin


class RefreshTokenModel(AuditMixin, Base):
    __tablename__ = "RefreshTokens"

    Id = Column(Integer, primary_key=True, index=True)
    UserId = Column(Integer, ForeignKey("Users.Id", ondelete="CASCADE"), nullable=False)
    Token = Column(String(512), nullable=False, unique=True)
    ExpiresAt = Column(DateTime(timezone=True), nullable=False)
    RevokedAt = Column(DateTime(timezone=True), nullable=True)
    ReplacedByToken = Column(String(512), nullable=True)
    IsRevoked = Column(Boolean, nullable=False, default=False)
