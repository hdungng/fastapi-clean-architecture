from typing import Any, Callable, Dict, Tuple, Type, TypeVar

TSource = TypeVar("TSource")
TDestination = TypeVar("TDestination")


class Mapper:
    def __init__(self):
        self._mappings: Dict[Tuple[Type[Any], Type[Any]], Callable[[Any], Any]] = {}

    def CreateMap(self, source_type: Type[TSource], dest_type: Type[TDestination]):
        def default_mapping(source: TSource) -> TDestination:
            data = {}
            for attr in dir(source):
                if attr.startswith("_"):
                    continue
                value = getattr(source, attr)
                if callable(value):
                    continue
                data[attr] = value

            if hasattr(dest_type, "model_validate"):
                return dest_type.model_validate(data)  # type: ignore

            return dest_type(**data)  # type: ignore

        self._mappings[(source_type, dest_type)] = default_mapping
        return self

    def Map(self, source: TSource, dest_type: Type[TDestination]) -> TDestination:
        mapping = self._mappings.get((type(source), dest_type))
        if not mapping:
            raise ValueError(f"No mapping configured from {type(source).__name__} to {dest_type.__name__}")
        return mapping(source)


MapperInstance = Mapper()


def ConfigureMappings():
    from app.infrastructure.mapping.WeatherForecastProfile import WeatherForecastProfile
    from app.infrastructure.mapping.UserProfile import UserProfile
    from app.infrastructure.mapping.ProductProfile import ProductProfile
    from app.infrastructure.mapping.RoleProfile import RoleProfile
    from app.infrastructure.mapping.PermissionProfile import PermissionProfile

    WeatherForecastProfile(MapperInstance)
    UserProfile(MapperInstance)
    ProductProfile(MapperInstance)
    RoleProfile(MapperInstance)
    PermissionProfile(MapperInstance)
