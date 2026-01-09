from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config.settings import get_settings

settings = get_settings()

DATABASE_URL = settings.DATABASE_URL

Base = declarative_base()

engine = create_engine(
    DATABASE_URL,
    future=True,
    echo=False,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


def InitDb():
    # Import models để đăng ký với Base.metadata
    from app.infrastructure.db.models import (
        user_model,
        weather_forecast_model,
        product_model,
        role_model,
        permission_model,
        user_role_model,
        role_permission_model,
        refresh_token_model,
    )  # noqa: F401
    Base.metadata.create_all(bind=engine)
