from datetime import date
from pydantic import BaseModel


class WeatherForecastDto(BaseModel):
    id: int | None = None
    date: date
    temperature_c: int
    summary: str | None = None
