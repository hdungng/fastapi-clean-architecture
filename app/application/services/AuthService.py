from datetime import datetime, timedelta
import secrets

from fastapi import HTTPException, status

from app.application.services.interfaces.IAuthService import IAuthService
from app.application.dtos.LoginRequestDto import LoginRequestDto
from app.application.dtos.TokenResponseDto import TokenResponseDto
from app.domain.repositories.IUnitOfWork import IUnitOfWork
from app.infrastructure.auth.PasswordHasher import VerifyPassword
from app.infrastructure.auth.JwtSettings import CreateAccessToken
from app.domain.entities.RefreshToken import RefreshToken
from app.config.settings import get_settings

_settings = get_settings()


class AuthService(IAuthService):
    def __init__(self, unit_of_work: IUnitOfWork):
        self._unit_of_work = unit_of_work

    async def Login(self, request: LoginRequestDto) -> TokenResponseDto:
        user = await self._unit_of_work.Users.GetByUserName(request.UserName)

        if user is None or not VerifyPassword(request.Password, user.PasswordHash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        roles = user.Roles or []

        access_token = CreateAccessToken(
            {
                "sub": str(user.Id),
                "username": user.UserName,
                "roles": roles,
            }
        )

        refresh_token_str: str | None = None
        if _settings.ENABLE_REFRESH_TOKEN:
            refresh_token_str = await self._IssueRefreshToken(user.Id)

        return TokenResponseDto(AccessToken=access_token, RefreshToken=refresh_token_str)

    async def _IssueRefreshToken(self, user_id: int) -> str:
        token = secrets.token_urlsafe(64)
        expires = datetime.utcnow() + timedelta(days=_settings.REFRESH_TOKEN_EXPIRE_DAYS)

        entity = RefreshToken(
            Id=None,
            UserId=user_id,
            Token=token,
            ExpiresAt=expires,
        )
        await self._unit_of_work.RefreshTokens.Add(entity)
        await self._unit_of_work.SaveChanges()
        return token

    async def Refresh(self, refresh_token: str) -> TokenResponseDto:
        if not _settings.ENABLE_REFRESH_TOKEN:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Refresh token is disabled by configuration",
            )

        existing = await self._unit_of_work.RefreshTokens.GetByToken(refresh_token)
        if existing is None or existing.IsRevoked or existing.ExpiresAt <= datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired refresh token",
            )

        user = await self._unit_of_work.Users.GetById(existing.UserId)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User for this token no longer exists",
            )

        roles = user.Roles or []

        access_token = CreateAccessToken(
            {
                "sub": str(user.Id),
                "username": user.UserName,
                "roles": roles,
            }
        )

        # Optionally: rotate refresh token
        new_refresh_token = await self._IssueRefreshToken(user.Id)
        existing.IsRevoked = True
        await self._unit_of_work.RefreshTokens.Revoke(existing)
        await self._unit_of_work.SaveChanges()

        return TokenResponseDto(AccessToken=access_token, RefreshToken=new_refresh_token)

    async def RevokeRefreshToken(self, refresh_token: str) -> None:
        existing = await self._unit_of_work.RefreshTokens.GetByToken(refresh_token)
        if existing is None:
            return
        await self._unit_of_work.RefreshTokens.Revoke(existing)
        await self._unit_of_work.SaveChanges()
