from typing import List, Optional
from app.application.services.interfaces.IWeatherForecastService import IWeatherForecastService
from app.application.dtos.WeatherForecastDto import WeatherForecastDto
from app.domain.repositories.IUnitOfWork import IUnitOfWork
from app.domain.entities.WeatherForecast import WeatherForecast
from app.infrastructure.mapping.AutoMapper import MapperInstance


class WeatherForecastService(IWeatherForecastService):
    """
    WeatherForecastService

    Convention:
    - Mỗi method tương ứng 1 use-case (business logic).
    - Không trả về ApiResponse trực tiếp, chỉ làm việc với DTO / entity.
    - Controller chịu trách nhiệm wrap kết quả vào ApiResponse.
    """

    def __init__(self, unit_of_work: IUnitOfWork):
        self._unit_of_work = unit_of_work

    async def GetAll(self) -> List[WeatherForecastDto]:
        """Lấy danh sách tất cả WeatherForecast dưới dạng DTO."""
        entities = await self._unit_of_work.WeatherForecasts.GetAll()
        return [MapperInstance.Map(e, WeatherForecastDto) for e in entities]

    async def GetById(self, id: int) -> Optional[WeatherForecastDto]:
        """Lấy WeatherForecast theo Id, trả về None nếu không tồn tại."""
        entity = await self._unit_of_work.WeatherForecasts.GetById(id)
        return MapperInstance.Map(entity, WeatherForecastDto) if entity else None

    async def Create(self, dto: WeatherForecastDto) -> WeatherForecastDto:
        """Tạo mới WeatherForecast từ DTO và trả về DTO đã được lưu."""
        entity = MapperInstance.Map(dto, WeatherForecast)
        created = await self._unit_of_work.WeatherForecasts.Add(entity)
        await self._unit_of_work.SaveChanges()
        return MapperInstance.Map(created, WeatherForecastDto)

    async def Update(self, id: int, dto: WeatherForecastDto) -> WeatherForecastDto:
        """Cập nhật WeatherForecast (Id lấy từ route, data từ DTO)."""
        entity = MapperInstance.Map(dto, WeatherForecast)
        entity.id = id
        updated = await self._unit_of_work.WeatherForecasts.Update(entity)
        await self._unit_of_work.SaveChanges()
        return MapperInstance.Map(updated, WeatherForecastDto)

    async def Delete(self, id: int) -> None:
        """Xoá WeatherForecast theo Id."""
        await self._unit_of_work.WeatherForecasts.Delete(id)
        await self._unit_of_work.SaveChanges()
