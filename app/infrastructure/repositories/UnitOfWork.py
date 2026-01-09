from app.domain.repositories.IUnitOfWork import IUnitOfWork
from app.domain.repositories.IWeatherForecastRepository import IWeatherForecastRepository
from app.domain.repositories.IUserRepository import IUserRepository
from app.domain.repositories.IProductRepository import IProductRepository
from app.domain.repositories.IRoleRepository import IRoleRepository
from app.domain.repositories.IPermissionRepository import IPermissionRepository
from app.domain.repositories.IRefreshTokenRepository import IRefreshTokenRepository
from app.infrastructure.db.DbContext import DbContext
from app.infrastructure.repositories.WeatherForecastRepository import WeatherForecastRepository
from app.infrastructure.repositories.UserRepository import UserRepository
from app.infrastructure.repositories.ProductRepository import ProductRepository
from app.infrastructure.repositories.RoleRepository import RoleRepository
from app.infrastructure.repositories.PermissionRepository import PermissionRepository
from app.infrastructure.repositories.RefreshTokenRepository import RefreshTokenRepository


class UnitOfWork(IUnitOfWork):
    def __init__(self, db_context: DbContext):
        self._db_context = db_context
        self.WeatherForecasts: IWeatherForecastRepository = WeatherForecastRepository(db_context.Session)
        self.Users: IUserRepository = UserRepository(db_context.Session)
        self.Products: IProductRepository = ProductRepository(db_context.Session)
        self.Roles: IRoleRepository = RoleRepository(db_context.Session)
        self.Permissions: IPermissionRepository = PermissionRepository(db_context.Session)
        self.RefreshTokens: IRefreshTokenRepository = RefreshTokenRepository(db_context.Session)

    async def SaveChanges(self) -> None:
        self._db_context.Session.commit()

    async def Dispose(self) -> None:
        self._db_context.Dispose()
