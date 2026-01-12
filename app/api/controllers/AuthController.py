from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.application.dtos.LoginRequestDto import LoginRequestDto
from app.application.dtos.TokenResponseDto import TokenResponseDto
from app.application.services.AuthService import AuthService
from app.application.services.interfaces.IAuthService import IAuthService
from app.infrastructure.auth.Dependencies import GetUnitOfWork
from app.domain.repositories.IUnitOfWork import IUnitOfWork
from app.shared.api_responses import Ok, BadRequest


router = APIRouter(prefix="/api/auth", tags=["Auth"])


def GetAuthService(unit_of_work: IUnitOfWork = Depends(GetUnitOfWork)) -> IAuthService:
    """Resolve IAuthService từ IUnitOfWork."""
    return AuthService(unit_of_work)


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
