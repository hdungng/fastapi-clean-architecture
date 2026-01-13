from typing import Optional
from fastapi import APIRouter, Depends

from app.application.dtos.UserDto import UserDto
from app.application.dtos.UserCreateDto import UserCreateDto
from app.application.services.UserService import UserService
from app.application.services.interfaces.IUserService import IUserService
from app.domain.repositories.IUnitOfWork import IUnitOfWork
from app.infrastructure.db.DbContext import DbContext
from app.infrastructure.repositories.UnitOfWork import UnitOfWork
from app.infrastructure.auth.Dependencies import GetCurrentUser
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
        "total": paged.total,
        "page": paged.page,
        "page_size": paged.page_size,
        "total_pages": paged.total_pages,
    }
    return Ok(paged.items, meta=meta)


@router.post("")
async def Create(
    dto: UserCreateDto,
    service: IUserService = Depends(GetService),
    current_user: UserDto = Depends(GetCurrentUser),
):
    """
    POST /api/users

    Summary:
    - Tạo mới user (có password + roles).

    Returns:
    - 201: ApiResponse[UserDto]
    """
    try:
        created = await service.Create(dto)
    except ValueError as ex:
        return BadRequest(str(ex))
    location = f"/api/users/{created.id}"
    return Created(location, created)


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
