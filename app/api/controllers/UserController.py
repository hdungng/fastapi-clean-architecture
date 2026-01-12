from typing import Optional, List
from fastapi import APIRouter, Depends

from app.application.dtos.UserDto import UserDto
from app.application.dtos.ChangePasswordDto import ChangePasswordDto
from app.application.dtos.UserRolesUpdateDto import UserRolesUpdateDto
from app.application.services.UserService import UserService
from app.application.services.interfaces.IUserService import IUserService
from app.domain.repositories.IUnitOfWork import IUnitOfWork
from app.infrastructure.db.DbContext import DbContext
from app.infrastructure.repositories.UnitOfWork import UnitOfWork
from app.infrastructure.auth.Dependencies import GetCurrentUser
from app.infrastructure.auth.Authorization import RequirePermissions, UserPrincipal
from app.shared.api_responses import Ok, NotFound, Created, BadRequest


router = APIRouter(prefix="/api/users", tags=["Users"])


def GetDbContext():
    """Factory DbContext cho mỗi request (giống AddDbContext)."""
    db = DbContext()
    try:
        yield db
    finally:
        db.Dispose()


def GetUnitOfWork(db: DbContext = Depends(GetDbContext)) -> IUnitOfWork:
    """Resolve IUnitOfWork dùng DbContext."""
    return UnitOfWork(db)


def GetService(uow: IUnitOfWork = Depends(GetUnitOfWork)) -> IUserService:
    """Resolve IUserService từ UnitOfWork."""
    return UserService(uow)


# -------- Existing admin-style endpoints --------


@router.get("")
async def GetUsers(
    page: int = 1,
    pageSize: int = 10,
    sortBy: Optional[str] = None,
    sortDir: str = "asc",
    search: Optional[str] = None,
    isActive: Optional[bool] = None,
    service: IUserService = Depends(GetService),
    current_user: UserDto = Depends(GetCurrentUser),
):
    """
    GET /api/users

    Summary:
    - Lấy danh sách người dùng có phân trang, sort, search, filter.

    Query:
    - page, pageSize: phân trang
    - sortBy, sortDir: sắp xếp
    - search: tìm kiếm theo user_name, email, full_name
    - isActive: filter theo trạng thái hoạt động

    Returns:
    - ApiResponse[List[UserDto]] với meta = thông tin phân trang
    """
    paged = await service.GetPaged(
        page=page,
        page_size=pageSize,
        sort_by=sortBy,
        sort_dir=sortDir,
        search=search,
        is_active=isActive,
    )
    meta = {
        "Total": paged.Total,
        "Page": paged.Page,
        "PageSize": paged.PageSize,
        "TotalPages": paged.TotalPages,
    }
    return Ok(paged.Items, meta=meta)


@router.get("/{id}")
async def GetById(
    id: int,
    service: IUserService = Depends(GetService),
    current_user: UserDto = Depends(GetCurrentUser),
):
    """
    GET /api/users/{id}

    Summary:
    - Lấy thông tin người dùng theo Id.

    Returns:
    - 200: ApiResponse[UserDto]
    - 404: User not found
    """
    result = await service.GetById(id)
    if not result:
        return NotFound("User not found")
    return Ok(result)


@router.post("")
async def Create(
    dto: UserDto,
    service: IUserService = Depends(GetService),
    current_user: UserDto = Depends(GetCurrentUser),
):
    """
    POST /api/users

    Summary:
    - Tạo mới user (DTO không chứa Password, phần login dùng password riêng).

    Returns:
    - 201: ApiResponse[UserDto]
    """
    if dto.id is not None:
        return BadRequest("id must be null when creating a new user")
    created = await service.Create(dto)
    location = f"/api/users/{created.id}"
    return Created(location, created)


@router.put("/{id}")
async def Update(
    id: int,
    dto: UserDto,
    service: IUserService = Depends(GetService),
    current_user: UserDto = Depends(GetCurrentUser),
):
    """
    PUT /api/users/{id}

    Summary:
    - Cập nhật thông tin user (trừ password).

    Returns:
    - 200: ApiResponse[UserDto]
    """
    updated = await service.Update(id, dto)
    return Ok(updated)


@router.delete("/{id}")
async def Delete(
    id: int,
    service: IUserService = Depends(GetService),
    current_user: UserDto = Depends(GetCurrentUser),
):
    """
    DELETE /api/users/{id}

    Summary:
    - Xoá user theo Id.

    Returns:
    - 200: ApiResponse với message trong data
    """
    await service.Delete(id)
    return Ok({"message": "User deleted"})


# -------- Current user self endpoints --------


@router.get("/me")
async def GetMe(
    service: IUserService = Depends(GetService),
    current_user: UserDto = Depends(GetCurrentUser),
):
    """
    GET /api/users/me

    Summary:
    - Lấy thông tin profile của chính user đang đăng nhập.
    """
    profile = await service.GetCurrentUserProfile(current_user.id)
    if not profile:
        return NotFound("User not found")
    return Ok(profile)


@router.get("/me/roles")
async def GetMyRoles(
    service: IUserService = Depends(GetService),
    current_user: UserDto = Depends(GetCurrentUser),
):
    """
    GET /api/users/me/roles

    Summary:
    - Lấy danh sách role name của chính user.
    """
    roles: List[str] = await service.GetCurrentUserRoles(current_user.id)
    return Ok(roles)


@router.get("/me/permissions")
async def GetMyPermissions(
    service: IUserService = Depends(GetService),
    current_user: UserDto = Depends(GetCurrentUser),
):
    """
    GET /api/users/me/permissions

    Summary:
    - Lấy danh sách permission name hiệu lực (từ tất cả roles của user).
    """
    perms: List[str] = await service.GetCurrentUserPermissions(current_user.id)
    return Ok(perms)


@router.put("/me/roles")
async def UpdateMyRoles(
    request: UserRolesUpdateDto,
    service: IUserService = Depends(GetService),
    principal: UserPrincipal = Depends(RequirePermissions("Users.Self.ManageRoles", enforce=True)),
):
    """
    PUT /api/users/me/roles

    Summary:
    - Cập nhật danh sách roles cho chính user.

    Authorization:
    - Permission bắt buộc: Users.Self.ManageRoles

    Body:
    - { "roles": ["Admin", "User"] }
    """
    try:
        updated = await service.UpdateCurrentUserRoles(principal.id, request.roles)
    except ValueError as ex:
        return BadRequest(str(ex))
    return Ok(updated)

@router.put("/me/password")
async def ChangeMyPassword(
    request: ChangePasswordDto,
    service: IUserService = Depends(GetService),
    current_user: UserDto = Depends(GetCurrentUser),
):
    """
    PUT /api/users/me/password

    Summary:
    - Đổi mật khẩu cho chính user.

    Body:
    - current_password: mật khẩu hiện tại
    - new_password: mật khẩu mới

    Rules:
    - Bắt buộc đúng current_password
    - Không yêu cầu permission đặc biệt, chỉ cần user đã đăng nhập
    """
    try:
        await service.ChangePassword(
            user_id=current_user.id,
            current_password=request.current_password,
            new_password=request.new_password,
        )
    except ValueError as ex:
        return BadRequest(str(ex))
    return Ok({"message": "Password changed successfully"})
