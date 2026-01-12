from sqlalchemy import Column, Integer, String, Date
from app.infrastructure.db.base import Base
from app.infrastructure.db.audit_mixin import AuditMixin


class WeatherForecastModel(AuditMixin, Base):
    __tablename__ = "WeatherForecasts"

    id = Column("Id", Integer, primary_key=True, index=True)
    date = Column("Date", Date, nullable=False)
    temperature_c = Column("TemperatureC", Integer, nullable=False)
    summary = Column("Summary", String(256), nullable=True)
