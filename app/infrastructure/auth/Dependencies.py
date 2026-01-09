from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, OAuth2PasswordBearer

from app.infrastructure.auth.JwtSettings import DecodeToken
from app.infrastructure.db.DbContext import DbContext
from app.infrastructure.repositories.UnitOfWork import UnitOfWork
from app.domain.repositories.IUnitOfWork import IUnitOfWork
from app.application.dtos.UserDto import UserDto
from app.infrastructure.mapping.AutoMapper import MapperInstance

bearer_scheme = HTTPBearer(auto_error=True)


def GetDbContext():
    db = DbContext()
    try:
        yield db
    finally:
        db.Dispose()


def GetUnitOfWork(db: DbContext = Depends(GetDbContext)) -> IUnitOfWork:
    return UnitOfWork(db)


def GetCurrentUser(
    creds: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> str:
    token = creds.credentials  # chính là access_token bạn dán vào Swagger
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return token