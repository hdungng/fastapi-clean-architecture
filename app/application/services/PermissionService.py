from typing import List

from app.application.dtos.PermissionDto import PermissionDto
from app.application.services.interfaces.IPermissionService import IPermissionService
from app.domain.entities.Permission import Permission
from app.domain.repositories.IUnitOfWork import IUnitOfWork
from app.infrastructure.mapping.AutoMapper import MapperInstance


class PermissionService(IPermissionService):
    """Service quản lý Permission + assign Role-Permission."""

    def __init__(self, unit_of_work: IUnitOfWork):
        self._unit_of_work = unit_of_work

    async def GetAll(self) -> List[PermissionDto]:
        entities = await self._unit_of_work.Permissions.GetAll()
        return [MapperInstance.Map(e, PermissionDto) for e in entities]

    async def GetById(self, id: int) -> PermissionDto | None:
        entity = await self._unit_of_work.Permissions.GetById(id)
        return MapperInstance.Map(entity, PermissionDto) if entity else None

    async def Create(self, dto: PermissionDto) -> PermissionDto:
        entity = MapperInstance.Map(dto, Permission)
        created = await self._unit_of_work.Permissions.Add(entity)
        await self._unit_of_work.SaveChanges()
        return MapperInstance.Map(created, PermissionDto)

    async def Update(self, id: int, dto: PermissionDto) -> PermissionDto:
        entity = MapperInstance.Map(dto, Permission)
        entity.id = id
        updated = await self._unit_of_work.Permissions.Update(entity)
        await self._unit_of_work.SaveChanges()
        return MapperInstance.Map(updated, PermissionDto)

    async def Delete(self, id: int) -> None:
        await self._unit_of_work.Permissions.Delete(id)
        await self._unit_of_work.SaveChanges()

    async def AssignPermissionToRole(self, permission_id: int, role_id: int) -> None:
        await self._unit_of_work.Permissions.AssignPermissionToRole(permission_id=permission_id, role_id=role_id)
        await self._unit_of_work.SaveChanges()

    async def RemovePermissionFromRole(self, permission_id: int, role_id: int) -> None:
        await self._unit_of_work.Permissions.RemovePermissionFromRole(permission_id=permission_id, role_id=role_id)
        await self._unit_of_work.SaveChanges()
