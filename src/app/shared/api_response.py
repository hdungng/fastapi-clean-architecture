from typing import Generic, Optional, TypeVar

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
