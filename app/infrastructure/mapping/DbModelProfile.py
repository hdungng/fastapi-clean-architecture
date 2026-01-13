from app.infrastructure.mapping.AutoMapper import Mapper
from app.domain.entities.Permission import Permission
from app.domain.entities.Product import Product
from app.domain.entities.RefreshToken import RefreshToken
from app.domain.entities.Role import Role
from app.domain.entities.User import User
from app.domain.entities.WeatherForecast import WeatherForecast
from app.infrastructure.db.models.permission_model import PermissionModel
from app.infrastructure.db.models.product_model import ProductModel
from app.infrastructure.db.models.refresh_token_model import RefreshTokenModel
from app.infrastructure.db.models.role_model import RoleModel
from app.infrastructure.db.models.user_model import UserModel
from app.infrastructure.db.models.weather_forecast_model import WeatherForecastModel


class DbModelProfile:
    def __init__(self, mapper: Mapper):
        mapper.CreateMap(
            RoleModel,
            Role,
            lambda model: Role(
                id=model.id,
                name=model.name,
                description=model.description,
                is_active=model.is_active,
            ),
        )
        mapper.CreateMap(
            Role,
            RoleModel,
            lambda entity: RoleModel(
                id=entity.id,
                name=entity.name,
                description=entity.description,
                is_active=entity.is_active,
            ),
        )
        mapper.CreateMap(
            UserModel,
            User,
            lambda model: User(
                id=model.id,
                user_name=model.user_name,
                email=model.email,
                full_name=model.full_name,
                is_active=model.is_active,
                password_hash=model.password_hash,
            ),
        )
        mapper.CreateMap(
            User,
            UserModel,
            lambda entity: UserModel(
                id=entity.id,
                user_name=entity.user_name,
                email=entity.email,
                full_name=entity.full_name,
                is_active=entity.is_active,
                password_hash=entity.password_hash,
            ),
        )
        mapper.CreateMap(
            PermissionModel,
            Permission,
            lambda model: Permission(
                id=model.id,
                name=model.name,
                description=model.description,
                is_active=model.is_active,
            ),
        )
        mapper.CreateMap(
            Permission,
            PermissionModel,
            lambda entity: PermissionModel(
                id=entity.id,
                name=entity.name,
                description=entity.description,
                is_active=entity.is_active,
            ),
        )
        mapper.CreateMap(
            ProductModel,
            Product,
            lambda model: Product(
                id=model.id,
                name=model.name,
                price=model.price,
                is_active=model.is_active,
            ),
        )
        mapper.CreateMap(
            Product,
            ProductModel,
            lambda entity: ProductModel(
                id=entity.id,
                name=entity.name,
                price=entity.price,
                is_active=entity.is_active,
            ),
        )
        mapper.CreateMap(
            WeatherForecastModel,
            WeatherForecast,
            lambda model: WeatherForecast(
                id=model.id,
                date=model.date,
                temperature_c=model.temperature_c,
                summary=model.summary,
            ),
        )
        mapper.CreateMap(
            WeatherForecast,
            WeatherForecastModel,
            lambda entity: WeatherForecastModel(
                id=entity.id,
                date=entity.date,
                temperature_c=entity.temperature_c,
                summary=entity.summary,
            ),
        )
        mapper.CreateMap(
            RefreshTokenModel,
            RefreshToken,
            lambda model: RefreshToken(
                id=model.id,
                user_id=model.user_id,
                token=model.token,
                expires_at=model.expires_at,
                revoked_at=model.revoked_at,
                replaced_by_token=model.replaced_by_token,
                is_revoked=model.is_revoked,
            ),
        )
        mapper.CreateMap(
            RefreshToken,
            RefreshTokenModel,
            lambda entity: RefreshTokenModel(
                id=entity.id,
                user_id=entity.user_id,
                token=entity.token,
                expires_at=entity.expires_at,
                revoked_at=entity.revoked_at,
                replaced_by_token=entity.replaced_by_token,
                is_revoked=entity.is_revoked,
            ),
        )
