from sqlalchemy import Column, DateTime, String, func


class AuditMixin:
    """Mixin cung cấp các trường audit cơ bản cho mọi entity."""

    created_at = Column("created_at", DateTime(timezone=True), server_default=func.now(), nullable=False)
    created_by = Column("created_by", String(100), nullable=True)
    updated_at = Column("updated_at", DateTime(timezone=True), onupdate=func.now())
    updated_by = Column("updated_by", String(100), nullable=True)
