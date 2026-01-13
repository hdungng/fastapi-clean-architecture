from datetime import date
from pydantic import BaseModel


class WeatherForecastCreateDto(BaseModel):
    date: date
    temperature_c: int
    summary: str | None = None
