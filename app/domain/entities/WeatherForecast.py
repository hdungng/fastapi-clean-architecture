from dataclasses import dataclass
from datetime import date


@dataclass
class WeatherForecast:
    date: date
    temperature_c: int
    id: int | None = None
    summary: str | None = None
