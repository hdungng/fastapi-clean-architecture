from typing import List, Optional
from sqlalchemy.orm import Session

from app.domain.repositories.IWeatherForecastRepository import IWeatherForecastRepository
from app.domain.entities.WeatherForecast import WeatherForecast
from app.infrastructure.db.models.weather_forecast_model import WeatherForecastModel


class WeatherForecastRepository(IWeatherForecastRepository):
    def __init__(self, session: Session):
        self._session = session

    async def GetAll(self) -> List[WeatherForecast]:
        rows = self._session.query(WeatherForecastModel).all()
        return [self._MapToEntity(r) for r in rows]

    async def GetById(self, id: int) -> Optional[WeatherForecast]:
        row = self._session.query(WeatherForecastModel).filter(WeatherForecastModel.Id == id).first()
        return self._MapToEntity(row) if row else None

    async def Add(self, entity: WeatherForecast) -> WeatherForecast:
        row = self._MapToModel(entity)
        self._session.add(row)
        self._session.flush()
        entity.Id = row.Id
        return entity

    async def Update(self, entity: WeatherForecast) -> WeatherForecast:
        row = self._session.query(WeatherForecastModel).filter(WeatherForecastModel.Id == entity.Id).first()
        if not row:
            raise KeyError("Not found")
        row.Date = entity.Date
        row.TemperatureC = entity.TemperatureC
        row.Summary = entity.Summary
        self._session.flush()
        return entity

    async def Delete(self, id: int) -> None:
        row = self._session.query(WeatherForecastModel).filter(WeatherForecastModel.Id == id).first()
        if row:
            self._session.delete(row)
            self._session.flush()

    def _MapToEntity(self, row: WeatherForecastModel) -> WeatherForecast:
        return WeatherForecast(Id=row.Id, Date=row.Date, TemperatureC=row.TemperatureC, Summary=row.Summary)

    def _MapToModel(self, entity: WeatherForecast) -> WeatherForecastModel:
        return WeatherForecastModel(Id=entity.Id, Date=entity.Date, TemperatureC=entity.TemperatureC, Summary=entity.Summary)
