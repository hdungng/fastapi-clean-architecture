from math import ceil
from typing import Generic, List, TypeVar

T = TypeVar("T")


class PagedResult(Generic[T]):
    def __init__(self, items: List[T], total: int, page: int, page_size: int):
        self.items = items
        self.total = total
        self.page = page
        self.page_size = page_size
        self.total_pages = ceil(total / page_size) if page_size else 0
