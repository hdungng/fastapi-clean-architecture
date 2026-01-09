from dataclasses import dataclass
from typing import List

from fastapi import Depends, HTTPException, status

from app.infrastructure.auth.Dependencies import GetCurrentUser, GetUnitOfWork
from app.application.dtos.UserDto import UserDto
from app.domain.repositories.IUnitOfWork import IUnitOfWork


@dataclass
class UserPrincipal:
    Id: int
    UserName: str
    Roles: List[str]


def BuildPrincipal(user: UserDto, roles: List[str] | None = None) -> UserPrincipal:
    resolved_roles = roles or user.Roles or []
    return UserPrincipal(
        Id=user.Id or 0,
        UserName=user.UserName,
        Roles=resolved_roles,
    )


def RequireRoles(*required_roles: str):
    """Dependency yêu cầu user phải có ít nhất một trong các role.

    - Giống [Authorize(Roles = "Admin,Manager")] trong ASP.NET Core.
    """

    async def dependency(
        user: UserDto = Depends(GetCurrentUser),
        uow: IUnitOfWork = Depends(GetUnitOfWork),
    ) -> UserPrincipal:
        roles = await uow.Roles.GetRolesByUser(user.Id)
        principal = BuildPrincipal(user, roles=[r.Name for r in roles])
        if required_roles:
            user_roles = set(principal.Roles)
            expected = set(required_roles)
            if user_roles.isdisjoint(expected):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Forbidden: insufficient role",
                )
        return principal

    return dependency


def RequirePermissions(*required_permissions: str, enforce: bool = True):
    """Dependency check permission mềm dẻo.

    - Nếu enforce=True: bắt buộc phải có tất cả permissions => 403 nếu thiếu
      (giống policy bắt buộc trong ASP.NET Core).
    - Nếu enforce=False: chỉ inject principal, không raise lỗi
      (dùng khi permission chỉ áp dụng conditionally trong business logic).
    """

    async def dependency(
        user: UserDto = Depends(GetCurrentUser),
        uow: IUnitOfWork = Depends(GetUnitOfWork),
    ) -> UserPrincipal:
        roles = await uow.Roles.GetRolesByUser(user.Id)
        principal = BuildPrincipal(user, roles=[r.Name for r in roles])
        if not required_permissions or not enforce:
            # Không bắt buộc, chỉ trả về principal để service tự xử lý tiếp.
            return principal

        perm_names: set[str] = set()
        for role in roles:
            perms = await uow.Permissions.GetPermissionsByRole(role.Id)
            for perm in perms:
                perm_names.add(perm.Name)
        user_permissions = perm_names
        missing = [p for p in required_permissions if p not in user_permissions]

        if missing:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Forbidden: missing permissions {missing}",
            )

        return principal

    return dependency
