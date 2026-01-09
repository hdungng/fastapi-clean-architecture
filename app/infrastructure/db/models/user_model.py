from sqlalchemy import Column, Integer, String, Boolean
from app.infrastructure.db.base import Base
from app.infrastructure.db.audit_mixin import AuditMixin


class UserModel(AuditMixin, Base):
    __tablename__ = "Users"

    Id = Column(Integer, primary_key=True, index=True)
    UserName = Column(String(100), nullable=False, unique=True)
    Email = Column(String(256), nullable=False, unique=True)
    FullName = Column(String(256), nullable=True)
    IsActive = Column(Boolean, nullable=False, default=True)
    PasswordHash = Column(String(256), nullable=True)
    Roles = Column(String(512), nullable=True)         # cache: 'Admin,User'
