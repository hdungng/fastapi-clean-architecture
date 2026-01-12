from sqlalchemy import Column, Integer, String, Boolean
from app.infrastructure.db.base import Base
from app.infrastructure.db.audit_mixin import AuditMixin


class UserModel(AuditMixin, Base):
    __tablename__ = "Users"

    id = Column("Id", Integer, primary_key=True, index=True)
    user_name = Column("UserName", String(100), nullable=False, unique=True)
    email = Column("Email", String(256), nullable=False, unique=True)
    full_name = Column("FullName", String(256), nullable=True)
    is_active = Column("IsActive", Boolean, nullable=False, default=True)
    password_hash = Column("PasswordHash", String(256), nullable=True)
    roles = Column("Roles", String(512), nullable=True)         # cache: 'Admin,User'
