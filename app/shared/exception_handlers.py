from typing import Any

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.shared.api_response import ApiResponse


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handle HTTPException (bao gồm 401, 403, 404, ...)."""
    message = exc.detail if isinstance(exc.detail, str) else str(exc.detail)

    payload = ApiResponse[Any](
        success=False,
        data=None,
        meta=None,
        message=message,
    )

    return JSONResponse(
        status_code=exc.status_code,
        content=payload.to_dict(),  # <- quan trọng
        headers=getattr(exc, "headers", None),
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Chuẩn hoá lỗi validate giống ModelState của ASP.NET Core."""
    errors: dict[str, list[str]] = {}

    for err in exc.errors():
        loc = err.get("loc", [])
        msg = err.get("msg", "")

        # loc thường dạng: ("body", "field") hoặc ("query", "page")
        if len(loc) > 1:
            field = ".".join(str(x) for x in loc[1:])
        elif len(loc) == 1:
            field = str(loc[0])
        else:
            field = ""

        errors.setdefault(field, []).append(msg)

    payload = ApiResponse[Any](
        success=False,
        data=None,
        meta=None,
        message="One or more validation errors occurred.",
        errors=errors,
    )

    return JSONResponse(
        status_code=422,
        content=payload.to_dict(),  # <- quan trọng
    )


async def unhandled_exception_handler(request: Request, exc: Exception):
    """Fallback cho mọi Exception chưa được bắt. Không lộ thông tin nội bộ ra ngoài."""
    payload = ApiResponse[Any](
        success=False,
        data=None,
        meta=None,
        message="Internal server error",
    )

    return JSONResponse(
        status_code=500,
        content=payload.to_dict(),  # <- quan trọng
    )
