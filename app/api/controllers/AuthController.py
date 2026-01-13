from typing import List
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.application.dtos.ChangePasswordDto import ChangePasswordDto
from app.application.dtos.LoginRequestDto import LoginRequestDto
from app.application.dtos.TokenResponseDto import TokenResponseDto
from app.application.dtos.UserDto import UserDto
from app.application.dtos.UserRolesUpdateDto import UserRolesUpdateDto
from app.application.services.AuthService import AuthService
from app.application.services.interfaces.IAuthService import IAuthService
from app.application.services.interfaces.IUserService import IUserService
from app.infrastructure.auth.Authorization import RequirePermissions, UserPrincipal
from app.infrastructure.auth.Dependencies import GetUnitOfWork, GetCurrentUser, GetService as ResolveUserService
from app.domain.repositories.IUnitOfWork import IUnitOfWork
from app.shared.api_responses import Ok, BadRequest, NotFound


router = APIRouter(prefix="/api/auth", tags=["Auth"])
self_router = APIRouter(prefix="/api/users", tags=["Auth"])


def GetAuthService(unit_of_work: IUnitOfWork = Depends(GetUnitOfWork)) -> IAuthService:
    """Resolve IAuthService từ IUnitOfWork."""
    return AuthService(unit_of_work)


def GetUserService(unit_of_work: IUnitOfWork = Depends(GetUnitOfWork)) -> IUserService:
    """Resolve IUserService từ IUnitOfWork."""
    return ResolveUserService(unit_of_work)


@router.post("/login")
async def Login(request: LoginRequestDto, service: IAuthService = Depends(GetAuthService)):
    """
    POST /api/auth/login

    - Đăng nhập, trả về access_token + (nếu bật) refresh_token.
    """
    token: TokenResponseDto = await service.Login(request)
    return Ok(token)


@router.post("/refresh")
async def RefreshToken(refreshToken: str, service: IAuthService = Depends(GetAuthService)):
    """
    POST /api/auth/refresh?refreshToken=...

    - Dùng refresh token để lấy access token mới.
    """
    if not refreshToken:
        return BadRequest("refreshToken is required")
    token: TokenResponseDto = await service.Refresh(refreshToken)
    return Ok(token)


@router.post("/revoke")
async def RevokeRefreshToken(refreshToken: str, service: IAuthService = Depends(GetAuthService)):
    """
    POST /api/auth/revoke?refreshToken=...

    - Revoke 1 refresh token cụ thể (không bắt buộc phải dùng cho mọi dự án).
    """
    if not refreshToken:
        return BadRequest("refreshToken is required")
    await service.RevokeRefreshToken(refreshToken)
    return Ok({"message": "Refresh token revoked"})

# (B) Token endpoint chuẩn OAuth2 để Swagger Authorize hoạt động
@router.post("/token")
async def Token(form_data: OAuth2PasswordRequestForm = Depends(),
                service: IAuthService = Depends(GetAuthService)):
    # map form -> DTO của bạn
    dto = LoginRequestDto(user_name=form_data.username, password=form_data.password)

    token: TokenResponseDto = await service.Login(dto)

    # Swagger yêu cầu đúng keys này
    return {"access_token": token.access_token, "token_type": "bearer"}
    # nếu DTO bạn đặt tên khác (AccessToken), đổi lại cho đúng:
    # return {"access_token": token.access_token, "token_type": "bearer"}


# -------- Current user self endpoints --------


@self_router.get("/me")
async def GetMe(
    service: IUserService = Depends(GetUserService),
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


@self_router.get("/me/roles")
async def GetMyRoles(
    service: IUserService = Depends(GetUserService),
    current_user: UserDto = Depends(GetCurrentUser),
):
    """
    GET /api/users/me/roles

    Summary:
    - Lấy danh sách role id của chính user.
    """
    roles: List[int] = await service.GetCurrentUserRoles(current_user.id)
    return Ok(roles)


@self_router.get("/me/permissions")
async def GetMyPermissions(
    service: IUserService = Depends(GetUserService),
    current_user: UserDto = Depends(GetCurrentUser),
):
    """
    GET /api/users/me/permissions

    Summary:
    - Lấy danh sách permission name hiệu lực (từ tất cả roles của user).
    """
    perms: List[str] = await service.GetCurrentUserPermissions(current_user.id)
    return Ok(perms)


@self_router.put("/me/roles")
async def UpdateMyRoles(
    request: UserRolesUpdateDto,
    service: IUserService = Depends(GetUserService),
    principal: UserPrincipal = Depends(RequirePermissions("Users.Self.ManageRoles", enforce=True)),
):
    """
    PUT /api/users/me/roles

    Summary:
    - Cập nhật danh sách roles cho chính user.

    Authorization:
    - Permission bắt buộc: Users.Self.ManageRoles

    Body:
    - { "roles": [1, 2] }
    """
    try:
        updated = await service.UpdateCurrentUserRoles(principal.id, request.roles)
    except ValueError as ex:
        return BadRequest(str(ex))
    return Ok(updated)


@self_router.put("/me/password")
async def ChangeMyPassword(
    request: ChangePasswordDto,
    service: IUserService = Depends(GetUserService),
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
