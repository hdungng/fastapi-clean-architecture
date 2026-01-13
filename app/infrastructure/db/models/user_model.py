from sqlalchemy import Column, Integer, String, Boolean
from app.infrastructure.db.base import Base
from app.infrastructure.db.audit_mixin import AuditMixin


class UserModel(AuditMixin, Base):
    __tablename__ = "users"

    id = Column("id", Integer, primary_key=True, index=True)
    user_name = Column("user_name", String(100), nullable=False, unique=True)
    email = Column("email", String(256), nullable=False, unique=True)
    full_name = Column("full_name", String(256), nullable=True)
    is_active = Column("is_active", Boolean, nullable=False, default=True)
    password_hash = Column("password_hash", String(256), nullable=True)
