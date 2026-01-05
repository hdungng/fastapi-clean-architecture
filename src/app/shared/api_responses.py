from fastapi import status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from app.shared.api_response import ApiResponse


def Ok(data=None, meta: dict | None = None):
    payload = ApiResponse(
        success=True,
        data=data,
        meta=meta,
    )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(payload),
    )


def Created(location: str, data=None, meta: dict | None = None):
    payload = ApiResponse(
        success=True,
        data=data,
        meta=meta,
    )
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=jsonable_encoder(payload),
        headers={"Location": location},
    )


def BadRequest(message: str = "Bad request", errors: dict | None = None):
    payload = ApiResponse(
        success=False,
        data=None,
        message=message,
        errors=errors,
    )
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder(payload),
    )


def NotFound(message: str = "Not found"):
    payload = ApiResponse(
        success=False,
        data=None,
        message=message,
    )
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=jsonable_encoder(payload),
    )
