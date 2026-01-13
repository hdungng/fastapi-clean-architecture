from sqlalchemy import Column, Integer, String, Date
from app.infrastructure.db.base import Base
from app.infrastructure.db.audit_mixin import AuditMixin


class WeatherForecastModel(AuditMixin, Base):
    __tablename__ = "weather_forecasts"

    id = Column("id", Integer, primary_key=True, index=True)
    date = Column("date", Date, nullable=False)
    temperature_c = Column("temperature_c", Integer, nullable=False)
    summary = Column("summary", String(256), nullable=True)
