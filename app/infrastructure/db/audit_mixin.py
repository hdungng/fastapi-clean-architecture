from sqlalchemy import Column, DateTime, String, func


class AuditMixin:
    """Mixin cung cấp các trường audit cơ bản cho mọi entity."""

    created_at = Column("CreatedAt", DateTime(timezone=True), server_default=func.now(), nullable=False)
    created_by = Column("CreatedBy", String(100), nullable=True)
    updated_at = Column("UpdatedAt", DateTime(timezone=True), onupdate=func.now())
    updated_by = Column("UpdatedBy", String(100), nullable=True)
