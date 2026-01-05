from fastapi import FastAPI

from app.api.controllers import AuthController
from app.api.controllers import WeatherForecastController
from app.api.controllers import UserController
from app.api.controllers import ProductController
from app.api.controllers import RoleController
from app.api.controllers import PermissionController


def RegisterRoutes(app: FastAPI) -> None:
    """
    Đăng ký tất cả API routes cho ứng dụng.

    Convention:
    - Mọi controller mới phải được include tại đây
    - Route prefix / tag được định nghĩa trong từng *Controller.py
    """
    app.include_router(AuthController.router)
    app.include_router(WeatherForecastController.router)
    app.include_router(UserController.router)
    app.include_router(ProductController.router)
    app.include_router(RoleController.router)
    app.include_router(PermissionController.router)
