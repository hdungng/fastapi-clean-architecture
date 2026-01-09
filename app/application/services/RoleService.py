from typing import List

from app.application.dtos.RoleDto import RoleDto
from app.application.services.interfaces.IRoleService import IRoleService
from app.domain.entities.Role import Role
from app.domain.repositories.IUnitOfWork import IUnitOfWork
from app.infrastructure.mapping.AutoMapper import MapperInstance


class RoleService(IRoleService):
    """Service quản lý Role + assign User-Role."""

    def __init__(self, unit_of_work: IUnitOfWork):
        self._unit_of_work = unit_of_work

    async def GetAll(self) -> List[RoleDto]:
        entities = await self._unit_of_work.Roles.GetAll()
        return [MapperInstance.Map(e, RoleDto) for e in entities]

    async def GetById(self, id: int) -> RoleDto | None:
        entity = await self._unit_of_work.Roles.GetById(id)
        return MapperInstance.Map(entity, RoleDto) if entity else None

    async def Create(self, dto: RoleDto) -> RoleDto:
        entity = MapperInstance.Map(dto, Role)
        created = await self._unit_of_work.Roles.Add(entity)
        await self._unit_of_work.SaveChanges()
        return MapperInstance.Map(created, RoleDto)

    async def Update(self, id: int, dto: RoleDto) -> RoleDto:
        entity = MapperInstance.Map(dto, Role)
        entity.Id = id
        updated = await self._unit_of_work.Roles.Update(entity)
        await self._unit_of_work.SaveChanges()
        return MapperInstance.Map(updated, RoleDto)

    async def Delete(self, id: int) -> None:
        await self._unit_of_work.Roles.Delete(id)
        await self._unit_of_work.SaveChanges()

    async def AssignRoleToUser(self, role_id: int, user_id: int) -> None:
        await self._unit_of_work.Roles.AssignRoleToUser(user_id=user_id, role_id=role_id)
        await self._unit_of_work.SaveChanges()

    async def RemoveRoleFromUser(self, role_id: int, user_id: int) -> None:
        await self._unit_of_work.Roles.RemoveRoleFromUser(user_id=user_id, role_id=role_id)
        await self._unit_of_work.SaveChanges()
