from sqlalchemy import Column, DateTime, String, func


class AuditMixin:
    """Mixin cung cấp các trường audit cơ bản cho mọi entity."""

    CreatedAt = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    CreatedBy = Column(String(100), nullable=True)
    UpdatedAt = Column(DateTime(timezone=True), onupdate=func.now())
    UpdatedBy = Column(String(100), nullable=True)
