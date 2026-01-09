from app.infrastructure.mapping.AutoMapper import Mapper
from app.domain.entities.WeatherForecast import WeatherForecast
from app.application.dtos.WeatherForecastDto import WeatherForecastDto


class WeatherForecastProfile:
    def __init__(self, mapper: Mapper):
        mapper.CreateMap(WeatherForecast, WeatherForecastDto)
        mapper.CreateMap(WeatherForecastDto, WeatherForecast)
