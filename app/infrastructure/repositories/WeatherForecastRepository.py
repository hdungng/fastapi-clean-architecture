from typing import List, Optional
from sqlalchemy.orm import Session

from app.domain.repositories.IWeatherForecastRepository import IWeatherForecastRepository
from app.domain.entities.WeatherForecast import WeatherForecast
from app.infrastructure.db.models.weather_forecast_model import WeatherForecastModel
from app.infrastructure.mapping.AutoMapper import MapperInstance


class WeatherForecastRepository(IWeatherForecastRepository):
    def __init__(self, session: Session):
        self._session = session

    async def GetAll(self) -> List[WeatherForecast]:
        rows = self._session.query(WeatherForecastModel).all()
        return [MapperInstance.Map(r, WeatherForecast) for r in rows]

    async def GetById(self, id: int) -> Optional[WeatherForecast]:
        row = self._session.query(WeatherForecastModel).filter(WeatherForecastModel.id == id).first()
        return MapperInstance.Map(row, WeatherForecast) if row else None

    async def Add(self, entity: WeatherForecast) -> WeatherForecast:
        row = MapperInstance.Map(entity, WeatherForecastModel)
        self._session.add(row)
        self._session.flush()
        entity.id = row.id
        return entity

    async def Update(self, entity: WeatherForecast) -> WeatherForecast:
        row = self._session.query(WeatherForecastModel).filter(WeatherForecastModel.id == entity.id).first()
        if not row:
            raise KeyError("Not found")
        row.date = entity.date
        row.temperature_c = entity.temperature_c
        row.summary = entity.summary
        self._session.flush()
        return entity

    async def Delete(self, id: int) -> None:
        row = self._session.query(WeatherForecastModel).filter(WeatherForecastModel.id == id).first()
        if row:
            self._session.delete(row)
            self._session.flush()
