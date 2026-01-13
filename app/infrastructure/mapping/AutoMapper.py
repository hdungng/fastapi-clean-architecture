from typing import Any, Callable, Dict, Tuple, Type, TypeVar
import inspect

TSource = TypeVar("TSource")
TDestination = TypeVar("TDestination")


class Mapper:
    def __init__(self):
        self._mappings: Dict[Tuple[Type[Any], Type[Any]], Callable[[Any], Any]] = {}

    def CreateMap(self, source_type: Type[TSource], dest_type: Type[TDestination]):
        def default_mapping(source: TSource) -> TDestination:
            # 1) Extract data safely from source
            if hasattr(source, "model_dump"):  # Pydantic v2 BaseModel
                data = source.model_dump(exclude_unset=True)
            elif hasattr(source, "dict"):  # Pydantic v1 BaseModel
                data = source.dict(exclude_unset=True)
            elif isinstance(source, dict):
                data = dict(source)
            else:
                # fallback: only instance attributes (NOT dir())
                data = dict(getattr(source, "__dict__", {}))

            # 2) If destination is a normal class/dataclass, filter keys by its __init__ params
            #    This prevents "unexpected keyword argument" errors.
            try:
                sig = inspect.signature(dest_type)
                allowed = set(sig.parameters.keys())
                data = {k: v for k, v in data.items() if k in allowed}
            except (TypeError, ValueError):
                # Some callables/types may not have a signature we can inspect
                pass

            # 3) If destination is Pydantic v2 model, validate/construct via model_validate
            if hasattr(dest_type, "model_validate"):
                return dest_type.model_validate(data)  # type: ignore

            # 4) Normal Python class/dataclass
            return dest_type(**data)  # type: ignore

        self._mappings[(source_type, dest_type)] = default_mapping
        return self

    def Map(self, source: TSource, dest_type: Type[TDestination]) -> TDestination:
        mapping = self._mappings.get((type(source), dest_type))
        if not mapping:
            raise ValueError(
                f"No mapping configured from {type(source).__name__} to {dest_type.__name__}"
            )
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
