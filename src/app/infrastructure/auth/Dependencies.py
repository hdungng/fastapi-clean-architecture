from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.infrastructure.auth.JwtSettings import DecodeToken
from app.infrastructure.db.DbContext import DbContext
from app.infrastructure.repositories.UnitOfWork import UnitOfWork
from app.domain.repositories.IUnitOfWork import IUnitOfWork
from app.application.dtos.UserDto import UserDto
from app.infrastructure.mapping.AutoMapper import MapperInstance

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def GetDbContext():
    db = DbContext()
    try:
        yield db
    finally:
        db.Dispose()


def GetUnitOfWork(db: DbContext = Depends(GetDbContext)) -> IUnitOfWork:
    return UnitOfWork(db)


async def GetCurrentUser(
    token: str = Depends(oauth2_scheme),
    unit_of_work: IUnitOfWork = Depends(GetUnitOfWork),
) -> UserDto:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = DecodeToken(token)
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except Exception:
        raise credentials_exception

    user = await unit_of_work.Users.GetById(int(user_id))
    if user is None:
        raise credentials_exception

    return MapperInstance.Map(user, UserDto)
