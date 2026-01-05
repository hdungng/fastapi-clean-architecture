from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.router import RegisterRoutes
from app.infrastructure.db.base import InitDb
from app.infrastructure.mapping.AutoMapper import ConfigureMappings
from app.shared.exception_handlers import (
    http_exception_handler,
    validation_exception_handler,
    unhandled_exception_handler,
)
from app.shared.logging_config import configure_logging, get_logger


def CreateApp() -> FastAPI:
    """
    Khởi tạo FastAPI app

    Convention:
    - Gọi InitDb() để đảm bảo DB, bảng đã được tạo
    - Gọi ConfigureMappings() để đăng ký AutoMapper profiles
    - Gọi configure_logging() để setup logging cho toàn app
    - Đăng ký global exception handlers
    - Đăng ký routes qua RegisterRoutes(app)
    """
    configure_logging()
    logger = get_logger(__name__)
    logger.info("Starting application...")

    app = FastAPI(
        title="FastAPI Clean Architecture Skeleton",
        version="1.0.0",
    )

    InitDb()
    ConfigureMappings()

    # Global exception handlers
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)

    # Đăng ký tất cả routers ở một chỗ
    RegisterRoutes(app)

    logger.info("Application started.")
    return app


app = CreateApp()
