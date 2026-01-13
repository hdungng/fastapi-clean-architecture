from typing import List, Optional
from sqlalchemy.orm import Session

from app.domain.repositories.IPermissionRepository import IPermissionRepository
from app.domain.entities.Permission import Permission
from app.infrastructure.db.models.permission_model import PermissionModel
from app.infrastructure.db.models.role_permission_model import RolePermissionModel
from app.infrastructure.mapping.AutoMapper import MapperInstance


class PermissionRepository(IPermissionRepository):
    def __init__(self, session: Session):
        self._session = session

    async def GetAll(self) -> List[Permission]:
        rows = self._session.query(PermissionModel).all()
        return [MapperInstance.Map(r, Permission) for r in rows]

    async def GetById(self, id: int) -> Optional[Permission]:
        row = self._session.query(PermissionModel).filter(PermissionModel.id == id).first()
        return MapperInstance.Map(row, Permission) if row else None

    async def GetByName(self, name: str) -> Optional[Permission]:
        row = self._session.query(PermissionModel).filter(PermissionModel.name == name).first()
        return MapperInstance.Map(row, Permission) if row else None

    async def Add(self, entity: Permission) -> Permission:
        row = MapperInstance.Map(entity, PermissionModel)
        self._session.add(row)
        self._session.flush()
        entity.id = row.id
        return entity

    async def Update(self, entity: Permission) -> Permission:
        row = self._session.query(PermissionModel).filter(PermissionModel.id == entity.id).first()
        if not row:
            raise KeyError("Permission not found")
        row.name = entity.name
        row.description = entity.description
        row.is_active = entity.is_active
        self._session.flush()
        return entity

    async def Delete(self, id: int) -> None:
        row = self._session.query(PermissionModel).filter(PermissionModel.id == id).first()
        if row:
            self._session.delete(row)
            self._session.flush()

    async def AssignPermissionToRole(self, permission_id: int, role_id: int) -> None:
        existing = (
            self._session.query(RolePermissionModel)
            .filter(RolePermissionModel.role_id == role_id, RolePermissionModel.permission_id == permission_id)
            .first()
        )
        if existing:
            return
        link = RolePermissionModel(role_id=role_id, permission_id=permission_id)
        self._session.add(link)
        self._session.flush()

    async def RemovePermissionFromRole(self, permission_id: int, role_id: int) -> None:
        link = (
            self._session.query(RolePermissionModel)
            .filter(RolePermissionModel.role_id == role_id, RolePermissionModel.permission_id == permission_id)
            .first()
        )
        if link:
            self._session.delete(link)
            self._session.flush()

    async def GetPermissionsByRole(self, role_id: int) -> List[Permission]:
        joins = (
            self._session.query(PermissionModel)
            .join(RolePermissionModel, RolePermissionModel.permission_id == PermissionModel.id)
            .filter(RolePermissionModel.role_id == role_id)
            .all()
        )
        return [MapperInstance.Map(r, Permission) for r in joins]
