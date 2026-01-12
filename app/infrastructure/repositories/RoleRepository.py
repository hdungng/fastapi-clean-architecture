from typing import List, Optional
from sqlalchemy.orm import Session

from app.domain.repositories.IRoleRepository import IRoleRepository
from app.domain.entities.Role import Role
from app.infrastructure.db.models.role_model import RoleModel
from app.infrastructure.db.models.user_role_model import UserRoleModel


class RoleRepository(IRoleRepository):
    def __init__(self, session: Session):
        self._session = session

    async def GetAll(self) -> List[Role]:
        rows = self._session.query(RoleModel).all()
        return [self._MapToEntity(r) for r in rows]

    async def GetById(self, id: int) -> Optional[Role]:
        row = self._session.query(RoleModel).filter(RoleModel.id == id).first()
        return self._MapToEntity(row) if row else None

    async def GetByName(self, name: str) -> Optional[Role]:
        row = self._session.query(RoleModel).filter(RoleModel.name == name).first()
        return self._MapToEntity(row) if row else None

    async def GetByNames(self, names: List[str]) -> List[Role]:
        if not names:
            return []
        rows = self._session.query(RoleModel).filter(RoleModel.name.in_(names)).all()
        return [self._MapToEntity(r) for r in rows]

    async def Add(self, entity: Role) -> Role:
        row = self._MapToModel(entity)
        self._session.add(row)
        self._session.flush()
        entity.id = row.id
        return entity

    async def Update(self, entity: Role) -> Role:
        row = self._session.query(RoleModel).filter(RoleModel.id == entity.id).first()
        if not row:
            raise KeyError("Role not found")
        row.name = entity.name
        row.description = entity.description
        row.is_active = entity.is_active
        self._session.flush()
        return entity

    async def Delete(self, id: int) -> None:
        row = self._session.query(RoleModel).filter(RoleModel.id == id).first()
        if row:
            self._session.delete(row)
            self._session.flush()

    async def AssignRoleToUser(self, user_id: int, role_id: int) -> None:
        existing = (
            self._session.query(UserRoleModel)
            .filter(UserRoleModel.user_id == user_id, UserRoleModel.role_id == role_id)
            .first()
        )
        if existing:
            return
        link = UserRoleModel(user_id=user_id, role_id=role_id)
        self._session.add(link)
        self._session.flush()

    async def RemoveRoleFromUser(self, user_id: int, role_id: int) -> None:
        link = (
            self._session.query(UserRoleModel)
            .filter(UserRoleModel.user_id == user_id, UserRoleModel.role_id == role_id)
            .first()
        )
        if link:
            self._session.delete(link)
            self._session.flush()

    async def ClearRolesForUser(self, user_id: int) -> None:
        self._session.query(UserRoleModel).filter(UserRoleModel.user_id == user_id).delete()
        self._session.flush()

    async def GetRolesByUser(self, user_id: int) -> List[Role]:
        joins = (
            self._session.query(RoleModel)
            .join(UserRoleModel, UserRoleModel.role_id == RoleModel.id)
            .filter(UserRoleModel.user_id == user_id)
            .all()
        )
        return [self._MapToEntity(r) for r in joins]

    def _MapToEntity(self, row: RoleModel) -> Role:
        return Role(
            id=row.id,
            name=row.name,
            description=row.description,
            is_active=row.is_active,
        )

    def _MapToModel(self, entity: Role) -> RoleModel:
        return RoleModel(
            id=entity.id,
            name=entity.name,
            description=entity.description,
            is_active=entity.is_active,
        )
