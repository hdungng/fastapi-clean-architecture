from abc import ABC, abstractmethod
from app.domain.repositories.IWeatherForecastRepository import IWeatherForecastRepository
from app.domain.repositories.IUserRepository import IUserRepository
from app.domain.repositories.IProductRepository import IProductRepository
from app.domain.repositories.IRoleRepository import IRoleRepository
from app.domain.repositories.IPermissionRepository import IPermissionRepository
from app.domain.repositories.IRefreshTokenRepository import IRefreshTokenRepository


class IUnitOfWork(ABC):
    WeatherForecasts: IWeatherForecastRepository
    Users: IUserRepository
    Products: IProductRepository
    Roles: IRoleRepository
    Permissions: IPermissionRepository
    RefreshTokens: IRefreshTokenRepository

    @abstractmethod
    async def SaveChanges(self) -> None:
        pass

    @abstractmethod
    async def Dispose(self) -> None:
        pass
