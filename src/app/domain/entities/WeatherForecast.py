from dataclasses import dataclass
from datetime import date


@dataclass
class WeatherForecast:
    Id: int | None
    Date: date
    TemperatureC: int
    Summary: str | None = None
