from typing import List
from fastapi import APIRouter, Depends

from app.application.dtos.RoleDto import RoleDto
from app.application.services.IRoleService import IRoleService
from app.application.services.RoleService import RoleService
from app.domain.repositories.IUnitOfWork import IUnitOfWork
from app.infrastructure.db.DbContext import DbContext
from app.infrastructure.repositories.UnitOfWork import UnitOfWork
from app.infrastructure.auth.Authorization import RequireRoles, UserPrincipal
from app.shared.api_responses import Ok, NotFound, Created, BadRequest


router = APIRouter(prefix="/api/roles", tags=["Roles"])


def GetDbContext():
    db = DbContext()
    try:
        yield db
    finally:
        db.Dispose()


def GetUnitOfWork(db: DbContext = Depends(GetDbContext)) -> IUnitOfWork:
    return UnitOfWork(db)


def GetService(uow: IUnitOfWork = Depends(GetUnitOfWork)) -> IRoleService:
    return RoleService(uow)


@router.get("")
async def GetRoles(
    service: IRoleService = Depends(GetService),
    principal: UserPrincipal = Depends(RequireRoles("Admin")),
):
    """GET /api/roles - lấy tất cả role (yêu cầu role Admin)."""
    items: List[RoleDto] = await service.GetAll()
    return Ok(items)


@router.get("/{id}")
async def GetRoleById(
    id: int,
    service: IRoleService = Depends(GetService),
    principal: UserPrincipal = Depends(RequireRoles("Admin")),
):
    result = await service.GetById(id)
    if not result:
        return NotFound("Role not found")
    return Ok(result)


@router.post("")
async def CreateRole(
    dto: RoleDto,
    service: IRoleService = Depends(GetService),
    principal: UserPrincipal = Depends(RequireRoles("Admin")),
):
    if dto.Id is not None:
        return BadRequest("Id must be null when creating a new role")
    created = await service.Create(dto)
    location = f"/api/roles/{created.Id}"
    return Created(location, created)


@router.put("/{id}")
async def UpdateRole(
    id: int,
    dto: RoleDto,
    service: IRoleService = Depends(GetService),
    principal: UserPrincipal = Depends(RequireRoles("Admin")),
):
    updated = await service.Update(id, dto)
    return Ok(updated)


@router.delete("/{id}")
async def DeleteRole(
    id: int,
    service: IRoleService = Depends(GetService),
    principal: UserPrincipal = Depends(RequireRoles("Admin")),
):
    await service.Delete(id)
    return Ok({"message": "Role deleted"})


@router.post("/{role_id}/users/{user_id}")
async def AssignRoleToUser(
    role_id: int,
    user_id: int,
    service: IRoleService = Depends(GetService),
    principal: UserPrincipal = Depends(RequireRoles("Admin")),
):
    await service.AssignRoleToUser(role_id=role_id, user_id=user_id)
    return Ok({"message": "Role assigned to user"})


@router.delete("/{role_id}/users/{user_id}")
async def RemoveRoleFromUser(
    role_id: int,
    user_id: int,
    service: IRoleService = Depends(GetService),
    principal: UserPrincipal = Depends(RequireRoles("Admin")),
):
    await service.RemoveRoleFromUser(role_id=role_id, user_id=user_id)
    return Ok({"message": "Role removed from user"})
