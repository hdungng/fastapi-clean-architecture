from datetime import date
from pydantic import BaseModel


class WeatherForecastDto(BaseModel):
    Id: int | None = None
    Date: date
    TemperatureC: int
    Summary: str | None = None
