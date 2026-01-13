from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, OAuth2PasswordBearer
from jose import jwt, JWTError
from app.application.services.UserService import UserService
from app.application.services.interfaces.IUserService import IUserService
from app.infrastructure.auth.JwtSettings import SECRET_KEY, DecodeToken
from app.infrastructure.db.DbContext import DbContext
from app.infrastructure.repositories.UnitOfWork import UnitOfWork
from app.domain.repositories.IUnitOfWork import IUnitOfWork
from app.application.dtos.UserDto import UserDto
from app.infrastructure.mapping.AutoMapper import MapperInstance

bearer_scheme = HTTPBearer(auto_error=True)
ALGORITHM = "HS256"

def GetDbContext():
    db = DbContext()
    try:
        yield db
    finally:
        db.Dispose()
        
def GetUnitOfWork(db: DbContext = Depends(GetDbContext)) -> IUnitOfWork:
    return UnitOfWork(db)

def GetService(uow: IUnitOfWork = Depends(GetUnitOfWork)) -> IUserService:
    """Resolve IUserService từ UnitOfWork."""
    return UserService(uow)


async def GetCurrentUser(
    creds: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    service: IUserService = Depends(GetService),
) -> UserDto:
    token = creds.credentials
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    # Thường user_id nằm ở "sub"
    sub = payload.get("sub")
    if not sub:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")

    # JWT hay để sub là string → convert về int
    try:
        user_id = int(sub)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user id in token")

    user = await service.GetById(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    return user