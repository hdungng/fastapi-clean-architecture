from typing import List, Optional
from sqlalchemy.orm import Session

from app.domain.repositories.IPermissionRepository import IPermissionRepository
from app.domain.entities.Permission import Permission
from app.infrastructure.db.models.permission_model import PermissionModel
from app.infrastructure.db.models.role_permission_model import RolePermissionModel


class PermissionRepository(IPermissionRepository):
    def __init__(self, session: Session):
        self._session = session

    async def GetAll(self) -> List[Permission]:
        rows = self._session.query(PermissionModel).all()
        return [self._MapToEntity(r) for r in rows]

    async def GetById(self, id: int) -> Optional[Permission]:
        row = self._session.query(PermissionModel).filter(PermissionModel.Id == id).first()
        return self._MapToEntity(row) if row else None

    async def GetByName(self, name: str) -> Optional[Permission]:
        row = self._session.query(PermissionModel).filter(PermissionModel.Name == name).first()
        return self._MapToEntity(row) if row else None

    async def Add(self, entity: Permission) -> Permission:
        row = self._MapToModel(entity)
        self._session.add(row)
        self._session.flush()
        entity.Id = row.Id
        return entity

    async def Update(self, entity: Permission) -> Permission:
        row = self._session.query(PermissionModel).filter(PermissionModel.Id == entity.Id).first()
        if not row:
            raise KeyError("Permission not found")
        row.Name = entity.Name
        row.Description = entity.Description
        row.IsActive = entity.IsActive
        self._session.flush()
        return entity

    async def Delete(self, id: int) -> None:
        row = self._session.query(PermissionModel).filter(PermissionModel.Id == id).first()
        if row:
            self._session.delete(row)
            self._session.flush()

    async def AssignPermissionToRole(self, permission_id: int, role_id: int) -> None:
        existing = (
            self._session.query(RolePermissionModel)
            .filter(RolePermissionModel.RoleId == role_id, RolePermissionModel.PermissionId == permission_id)
            .first()
        )
        if existing:
            return
        link = RolePermissionModel(RoleId=role_id, PermissionId=permission_id)
        self._session.add(link)
        self._session.flush()

    async def RemovePermissionFromRole(self, permission_id: int, role_id: int) -> None:
        link = (
            self._session.query(RolePermissionModel)
            .filter(RolePermissionModel.RoleId == role_id, RolePermissionModel.PermissionId == permission_id)
            .first()
        )
        if link:
            self._session.delete(link)
            self._session.flush()

    async def GetPermissionsByRole(self, role_id: int) -> List[Permission]:
        joins = (
            self._session.query(PermissionModel)
            .join(RolePermissionModel, RolePermissionModel.PermissionId == PermissionModel.Id)
            .filter(RolePermissionModel.RoleId == role_id)
            .all()
        )
        return [self._MapToEntity(r) for r in joins]

    def _MapToEntity(self, row: PermissionModel) -> Permission:
        return Permission(
            Id=row.Id,
            Name=row.Name,
            Description=row.Description,
            IsActive=row.IsActive,
        )

    def _MapToModel(self, entity: Permission) -> PermissionModel:
        return PermissionModel(
            Id=entity.Id,
            Name=entity.Name,
            Description=entity.Description,
            IsActive=entity.IsActive,
        )
