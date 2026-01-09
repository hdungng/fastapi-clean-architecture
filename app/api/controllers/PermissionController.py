from typing import List
from fastapi import APIRouter, Depends

from app.application.dtos.PermissionDto import PermissionDto
from app.application.services.interfaces.IPermissionService import IPermissionService
from app.application.services.PermissionService import PermissionService
from app.domain.repositories.IUnitOfWork import IUnitOfWork
from app.infrastructure.db.DbContext import DbContext
from app.infrastructure.repositories.UnitOfWork import UnitOfWork
from app.infrastructure.auth.Authorization import RequireRoles, UserPrincipal
from app.shared.api_responses import Ok, NotFound, Created, BadRequest


router = APIRouter(prefix="/api/permissions", tags=["Permissions"])


def GetDbContext():
    db = DbContext()
    try:
        yield db
    finally:
        db.Dispose()


def GetUnitOfWork(db: DbContext = Depends(GetDbContext)) -> IUnitOfWork:
    return UnitOfWork(db)


def GetService(uow: IUnitOfWork = Depends(GetUnitOfWork)) -> IPermissionService:
    return PermissionService(uow)


@router.get("")
async def GetPermissions(
    service: IPermissionService = Depends(GetService),
    principal: UserPrincipal = Depends(RequireRoles("Admin")),
):
    """GET /api/permissions - lấy tất cả permission (yêu cầu role Admin)."""
    items: List[PermissionDto] = await service.GetAll()
    return Ok(items)


@router.get("/{id}")
async def GetPermissionById(
    id: int,
    service: IPermissionService = Depends(GetService),
    principal: UserPrincipal = Depends(RequireRoles("Admin")),
):
    result = await service.GetById(id)
    if not result:
        return NotFound("Permission not found")
    return Ok(result)


@router.post("")
async def CreatePermission(
    dto: PermissionDto,
    service: IPermissionService = Depends(GetService),
    principal: UserPrincipal = Depends(RequireRoles("Admin")),
):
    if dto.Id is not None:
        return BadRequest("Id must be null when creating a new permission")
    created = await service.Create(dto)
    location = f"/api/permissions/{created.Id}"
    return Created(location, created)


@router.put("/{id}")
async def UpdatePermission(
    id: int,
    dto: PermissionDto,
    service: IPermissionService = Depends(GetService),
    principal: UserPrincipal = Depends(RequireRoles("Admin")),
):
    updated = await service.Update(id, dto)
    return Ok(updated)


@router.delete("/{id}")
async def DeletePermission(
    id: int,
    service: IPermissionService = Depends(GetService),
    principal: UserPrincipal = Depends(RequireRoles("Admin")),
):
    await service.Delete(id)
    return Ok({"message": "Permission deleted"})


@router.post("/assign")
async def AssignPermissionToRole(
    roleId: int,
    permissionId: int,
    service: IPermissionService = Depends(GetService),
    principal: UserPrincipal = Depends(RequireRoles("Admin")),
):
    """Gán permission cho role: POST /api/permissions/assign?roleId=1&permissionId=2"""
    await service.AssignPermissionToRole(permission_id=permissionId, role_id=roleId)
    return Ok({"message": "Permission assigned to role"})


@router.delete("/unassign")
async def RemovePermissionFromRole(
    roleId: int,
    permissionId: int,
    service: IPermissionService = Depends(GetService),
    principal: UserPrincipal = Depends(RequireRoles("Admin")),
):
    """Xoá permission khỏi role: DELETE /api/permissions/unassign?roleId=1&permissionId=2"""
    await service.RemovePermissionFromRole(permission_id=permissionId, role_id=roleId)
    return Ok({"message": "Permission removed from role"})
