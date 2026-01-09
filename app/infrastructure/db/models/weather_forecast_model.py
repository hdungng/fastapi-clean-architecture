from sqlalchemy import Column, Integer, String, Date
from app.infrastructure.db.base import Base
from app.infrastructure.db.audit_mixin import AuditMixin


class WeatherForecastModel(AuditMixin, Base):
    __tablename__ = "WeatherForecasts"

    Id = Column(Integer, primary_key=True, index=True)
    Date = Column(Date, nullable=False)
    TemperatureC = Column(Integer, nullable=False)
    Summary = Column(String(256), nullable=True)
