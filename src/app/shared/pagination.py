from math import ceil
from typing import Generic, List, TypeVar

T = TypeVar("T")


class PagedResult(Generic[T]):
    def __init__(self, items: List[T], total: int, page: int, page_size: int):
        self.Items = items
        self.Total = total
        self.Page = page
        self.PageSize = page_size
        self.TotalPages = ceil(total / page_size) if page_size else 0
