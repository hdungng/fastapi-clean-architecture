from dataclasses import dataclass
from datetime import date


@dataclass
class WeatherForecast:
    id: int | None
    date: date
    temperature_c: int
    summary: str | None = None
