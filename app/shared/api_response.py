from __future__ import annotations

from typing import Any, Generic, Optional, TypeVar

T = TypeVar("T")


class ApiResponse(Generic[T]):
    def __init__(
        self,
        data: T | None = None,
        success: bool = True,
        meta: Optional[dict] = None,
        message: str | None = None,
        errors: Optional[dict[str, list[str]]] = None,
    ):
        self.success = success
        self.data = data
        self.meta = meta
        self.message = message
        self.errors = errors

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "success": self.success,
            "data": self.data,
            "meta": self.meta,
        }    
        if not self.success:
            if self.message is not None:
                payload["message"] = self.message
            if self.errors is not None:
                payload["errors"] = self.errors    
        return payload

