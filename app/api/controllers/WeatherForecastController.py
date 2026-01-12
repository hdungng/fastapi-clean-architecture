from fastapi import APIRouter, Depends

from app.application.dtos.WeatherForecastDto import WeatherForecastDto
from app.application.services.WeatherForecastService import WeatherForecastService
from app.application.services.interfaces.IWeatherForecastService import IWeatherForecastService
from app.domain.repositories.IUnitOfWork import IUnitOfWork
from app.infrastructure.db.DbContext import DbContext
from app.infrastructure.repositories.UnitOfWork import UnitOfWork
from app.shared.api_responses import Ok, NotFound, Created


router = APIRouter(prefix="/api/weather-forecasts", tags=["WeatherForecasts"])


def GetDbContext():
    """Factory DbContext cho mỗi request (giống AddDbContext trong ASP.NET Core)."""
    db = DbContext()
    try:
        yield db
    finally:
        db.Dispose()


def GetUnitOfWork(db: DbContext = Depends(GetDbContext)) -> IUnitOfWork:
    """Resolve IUnitOfWork thông qua DbContext (pattern UnitOfWork)."""
    return UnitOfWork(db)


def GetService(uow: IUnitOfWork = Depends(GetUnitOfWork)) -> IWeatherForecastService:
    """Resolve IWeatherForecastService từ IUnitOfWork (giống DI container)."""
    return WeatherForecastService(uow)


@router.get("")
async def GetAll(service: IWeatherForecastService = Depends(GetService)):
    """
    GET /api/weather-forecasts

    Summary:
    - Lấy danh sách tất cả WeatherForecast.

    Returns:
    - ApiResponse[List[WeatherForecastDto]]
    """
    result = await service.GetAll()
    return Ok(result)


@router.get("/{id}")
async def GetById(id: int, service: IWeatherForecastService = Depends(GetService)):
    """
    GET /api/weather-forecasts/{id}

    Summary:
    - Lấy thông tin WeatherForecast theo Id.

    Returns:
    - 200: ApiResponse[WeatherForecastDto]
    - 404: ApiResponse với message = "WeatherForecast not found"
    """
    result = await service.GetById(id)
    if not result:
        return NotFound("WeatherForecast not found")
    return Ok(result)


@router.post("")
async def Create(dto: WeatherForecastDto, service: IWeatherForecastService = Depends(GetService)):
    """
    POST /api/weather-forecasts

    Summary:
    - Tạo mới WeatherForecast.

    Body:
    - WeatherForecastDto (không cần id).

    Returns:
    - 201: ApiResponse[WeatherForecastDto] + header Location
    """
    created = await service.Create(dto)
    location = f"/api/weather-forecasts/{created.id}"
    return Created(location, created)


@router.put("/{id}")
async def Update(id: int, dto: WeatherForecastDto, service: IWeatherForecastService = Depends(GetService)):
    """
    PUT /api/weather-forecasts/{id}

    Summary:
    - Cập nhật WeatherForecast theo Id.

    Returns:
    - 200: ApiResponse[WeatherForecastDto]
    """
    updated = await service.Update(id, dto)
    return Ok(updated)


@router.delete("/{id}")
async def Delete(id: int, service: IWeatherForecastService = Depends(GetService)):
    """
    DELETE /api/weather-forecasts/{id}

    Summary:
    - Xoá WeatherForecast theo Id.

    Returns:
    - 200: ApiResponse với message trong data
    """
    await service.Delete(id)
    return Ok({"message": "WeatherForecast deleted"})
